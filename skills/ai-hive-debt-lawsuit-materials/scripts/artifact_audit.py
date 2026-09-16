#!/usr/bin/env python3
"""Local, standard-library-only source fingerprinting and artifact structure audit.

Python 3.9+ on systems supporting POSIX dir_fd and O_NOFOLLOW (macOS/Linux).
No network access, recursive discovery, document conversion or paid services.

  python3 artifact_audit.py sources --input FILE --input FILE --output manifest.json
  python3 artifact_audit.py verify --directory DIR --spec skill-spec.json --output audit.json

The spec must be a JSON object with a nonempty ``artifact_files`` string array.
All artifact names are literal, safe, relative paths, not globs or descriptions.
Output parents must already exist; outputs are exclusively created, never replaced.
Source IDs follow the explicit --input order; no source names, paths or content
are put into the manifest. Keep any private ID-to-file mapping separately.

Exit codes: 0 = requested mechanical checks passed; 1 = artifact failures or
unsupported formats; 2 = unsafe paths, invalid invocation/spec, or I/O failure.
Even exit 0 does NOT certify completeness of a file format, rendered appearance,
source authenticity, useful content, or legal/financial/professional correctness.
"""

import argparse
import csv
import errno
import hashlib
import io
import json
import math
import os
import re
import stat
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import PurePosixPath
from xml.etree import ElementTree as ET


SCHEMA_VERSION = 1
MAX_SPEC_BYTES = 1024 * 1024
MAX_PARSE_BYTES = 32 * 1024 * 1024
MAX_ZIP_MEMBERS = 4096
MAX_ZIP_UNCOMPRESSED = 64 * 1024 * 1024
MAX_XML_MEMBER_BYTES = 16 * 1024 * 1024
LIMITATION = (
    "Mechanical presence and limited format-structure checks only. "
    "Not verification of source authenticity, rendered appearance, content "
    "completeness, factual accuracy or professional correctness."
)


class AuditError(Exception):
    """Fixed, path-free error text suitable for a privacy-preserving CLI."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def _fail(code, message):
    raise AuditError(code, message)


def _os_error(exc):
    if exc.errno == errno.ENOENT:
        _fail("file_missing", "A requested file or parent directory is missing.")
    if exc.errno in (errno.ELOOP, errno.ENOTDIR):
        _fail("unsafe_path", "A path includes a symlink or non-directory parent.")
    if exc.errno == errno.EEXIST:
        _fail("output_exists", "Output already exists; choose a new output file.")
    _fail("io_error", "A local file operation failed; check access and available space.")


def _require_secure_open():
    if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
        _fail("unsupported_platform", "This platform lacks secure no-follow file access.")


def _absolute_parts(path):
    value = os.fspath(path)
    if not value or "\x00" in value or "\\" in value:
        _fail("unsafe_path", "Empty, NUL or backslash paths are not supported.")
    if ".." in value.split("/"):
        _fail("unsafe_path", "Parent-directory traversal is not allowed.")
    absolute = os.path.abspath(value)
    return absolute, [part for part in absolute.split("/") if part]


def _directory_fd(parts):
    _require_secure_open()
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    flags |= getattr(os, "O_CLOEXEC", 0)
    current = os.open("/", flags)
    try:
        for part in parts:
            # lstat improves diagnostics; O_NOFOLLOW still closes the race.
            info = os.stat(part, dir_fd=current, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                _fail("symlink_forbidden", "Symbolic links are not allowed.")
            next_fd = os.open(part, flags, dir_fd=current)
            os.close(current)
            current = next_fd
        return current
    except AuditError:
        os.close(current)
        raise
    except OSError as exc:
        os.close(current)
        _os_error(exc)


def _parent_fd(path):
    absolute, parts = _absolute_parts(path)
    if not parts:
        _fail("not_regular_file", "A regular file is required.")
    return _directory_fd(parts[:-1]), parts[-1], absolute


def _open_file(path):
    parent_fd, leaf, _ = _parent_fd(path)
    fd = None
    try:
        info = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        if stat.S_ISLNK(info.st_mode):
            _fail("symlink_forbidden", "Symbolic links are not allowed.")
        if not stat.S_ISREG(info.st_mode):
            _fail("not_regular_file", "A regular file is required.")
        flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(leaf, flags, dir_fd=parent_fd)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            _fail("not_regular_file", "A regular file is required.")
        stream = os.fdopen(fd, "rb")
        fd = None
        return stream
    except OSError as exc:
        _os_error(exc)
    finally:
        if fd is not None:
            os.close(fd)
        os.close(parent_fd)


def _stat_identity(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _read_file(path, limit):
    with _open_file(path) as stream:
        before = os.fstat(stream.fileno())
        if before.st_size > limit:
            _fail("inspection_limit_exceeded", "File exceeds this check's bounded parsing limit.")
        data = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    if len(data) > limit:
        _fail("inspection_limit_exceeded", "File exceeds this check's bounded parsing limit.")
    if _stat_identity(before) != _stat_identity(after) or len(data) != after.st_size:
        _fail("file_changed", "A file changed during inspection; retry with a stable copy.")
    return data


def _output_available(path):
    parent_fd, leaf, _ = _parent_fd(path)
    try:
        try:
            os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        _fail("output_exists", "Output already exists; choose a new output file.")
    finally:
        os.close(parent_fd)


def _write_json_exclusive(path, report):
    data = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    parent_fd, leaf, _ = _parent_fd(path)
    fd = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        fd = os.open(leaf, flags, 0o600, dir_fd=parent_fd)
        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as exc:
        _os_error(exc)
    finally:
        if fd is not None:
            os.close(fd)
        os.close(parent_fd)


def source_manifest(inputs):
    records = []
    for index, path in enumerate(inputs, 1):
        digest = hashlib.sha256()
        size = 0
        with _open_file(path) as stream:
            before = os.fstat(stream.fileno())
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
                size += len(block)
            after = os.fstat(stream.fileno())
        if _stat_identity(before) != _stat_identity(after) or size != after.st_size:
            _fail("file_changed", "A source changed while hashing; retry with a stable copy.")
        records.append({"source_id": "source-%04d" % index, "bytes": size, "sha256": digest.hexdigest()})
    if not records:
        _fail("invalid_input", "At least one explicit source file is required.")
    return {"schema_version": SCHEMA_VERSION, "kind": "source_fingerprints", "source_count": len(records),
            "source_order": "IDs follow explicit --input argument order; names and paths are omitted.",
            "sources": records,
            "limitation": "SHA256 proves byte equality only, not authenticity, provenance or accuracy."}


def _text(data):
    try:
        value = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        _fail("invalid_utf8", "This check requires UTF-8 text; convert an authorized copy explicitly.")
    if any(ord(char) < 32 and char not in "\t\n\r" for char in value):
        _fail("binary_in_text", "Unexpected control bytes in a text-format artifact.")
    return value


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("duplicate_json_key", "Duplicate JSON object keys are not accepted.")
        result[key] = value
    return result


def _constant(_value):
    _fail("invalid_json_number", "NaN and Infinity are not standard JSON numbers.")


def _json(data):
    try:
        return json.loads(_text(data), object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, RecursionError):
        _fail("invalid_json", "JSON could not be parsed.")


def _xml(data):
    # Decode first to avoid UTF-16 DOCTYPE bypasses in the declaration guard.
    value = _text(data)
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", value, flags=re.I):
        _fail("xml_declaration_forbidden", "DTD and entity declarations are not accepted.")
    try:
        return ET.fromstring(value)
    except (ET.ParseError, ValueError, RecursionError):
        _fail("invalid_xml", "XML could not be parsed.")


def _csv(data, delimiter=","):
    try:
        rows = csv.reader(io.StringIO(_text(data), newline=""), delimiter=delimiter, strict=True)
        header = next(rows, None)
        if not header or any(not field.strip() for field in header):
            _fail("invalid_csv_header", "CSV/TSV needs nonempty column names.")
        normalized = [field.strip().casefold() for field in header]
        if len(normalized) != len(set(normalized)):
            _fail("invalid_csv_header", "CSV/TSV column names must be unique.")
        count = 0
        for row in rows:
            if len(row) != len(header):
                _fail("csv_column_mismatch", "CSV/TSV rows must match the header column count.")
            count += 1
        return {"columns": len(header), "data_rows": count}
    except csv.Error:
        _fail("invalid_csv", "CSV/TSV quoting or field structure is invalid.")


class _HTMLStructure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.start_html = 0
        self.end_html = 0

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            self.start_html += 1

    def handle_endtag(self, tag):
        if tag == "html":
            self.end_html += 1


def _html(data):
    parser = _HTMLStructure()
    parser.feed(_text(data))
    parser.close()
    if parser.start_html != 1 or parser.end_html != 1:
        _fail("invalid_html_shell", "HTML must contain one actual opening and closing html element.")
    return {"check_scope": "HTML shell only; not browser rendering, scripting or full conformance."}


def _geojson(obj):
    def position(value):
        return (isinstance(value, list) and len(value) >= 2
                and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                        and (not isinstance(v, float) or math.isfinite(v)) for v in value))

    def coordinates(value, depth, minimum=0, ring=False):
        if depth == 0:
            return position(value)
        if not isinstance(value, list) or len(value) < minimum:
            return False
        if not all(coordinates(v, depth - 1) for v in value):
            return False
        return not ring or (len(value) >= 4 and value[0] == value[-1])

    def geometry(value, depth):
        if depth > 64 or not isinstance(value, dict):
            return False
        kind = value.get("type")
        coords = value.get("coordinates")
        if kind == "GeometryCollection":
            return isinstance(value.get("geometries"), list) and all(geometry(g, depth + 1) for g in value["geometries"])
        if kind == "Point":
            return position(coords)
        if kind == "MultiPoint":
            return coordinates(coords, 1)
        if kind == "LineString":
            return coordinates(coords, 1, minimum=2)
        if kind == "MultiLineString":
            return isinstance(coords, list) and all(coordinates(v, 1, minimum=2) for v in coords)
        if kind == "Polygon":
            return isinstance(coords, list) and all(coordinates(v, 1, ring=True) for v in coords)
        if kind == "MultiPolygon":
            return isinstance(coords, list) and all(isinstance(p, list) and all(coordinates(r, 1, ring=True) for r in p) for p in coords)
        return False

    def feature(value):
        return (isinstance(value, dict) and value.get("type") == "Feature"
                and "geometry" in value and "properties" in value
                and (value["properties"] is None or isinstance(value["properties"], dict))
                and (value["geometry"] is None or geometry(value["geometry"], 0)))

    if not isinstance(obj, dict):
        _fail("invalid_geojson", "GeoJSON needs a typed object.")
    kind = obj.get("type")
    valid = (isinstance(obj.get("features"), list) and all(feature(v) for v in obj["features"])) if kind == "FeatureCollection" else feature(obj) if kind == "Feature" else geometry(obj, 0)
    if not valid:
        _fail("invalid_geojson", "GeoJSON type, feature fields or coordinate shape is invalid.")
    return {"geojson_type": kind, "check_scope": "Basic type and coordinate shapes; not location accuracy, topology or CRS verification."}


def _graphml(root):
    namespace = "{http://graphml.graphdrawing.org/xmlns}"
    if root.tag != namespace + "graphml":
        _fail("invalid_graphml", "GraphML needs the graphml root and GraphML namespace.")
    graphs = list(root.iter(namespace + "graph"))
    if not graphs or any(g.get("edgedefault") not in ("directed", "undirected") for g in graphs):
        _fail("invalid_graphml", "GraphML needs a graph with an edgedefault value.")
    nodes = list(root.iter(namespace + "node"))
    ids = [node.get("id") for node in nodes]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        _fail("invalid_graphml", "GraphML node IDs must be present and unique.")
    ids = set(ids)
    edges = list(root.iter(namespace + "edge"))
    if any(edge.get("source") not in ids or edge.get("target") not in ids for edge in edges):
        _fail("invalid_graphml", "GraphML edges must reference existing node IDs.")
    return {"nodes": len(nodes), "edges": len(edges), "check_scope": "Basic graph structure; not full GraphML schema validation."}


OOXML = {
    ".docx": ("word/document.xml", "http://schemas.openxmlformats.org/wordprocessingml/2006/main", "document", "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"),
    ".xlsx": ("xl/workbook.xml", "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "workbook", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"),
    ".pptx": ("ppt/presentation.xml", "http://schemas.openxmlformats.org/presentationml/2006/main", "presentation", "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"),
}


def _member_path(name):
    if not name or "\\" in name or name.startswith("/") or ":" in name:
        return False
    parts = name.rstrip("/").split("/")
    return all(part not in ("", ".", "..") for part in parts)


def _ooxml(data, suffix):
    main, namespace, local_root, content_type = OOXML[suffix]
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) > MAX_ZIP_MEMBERS or sum(i.file_size for i in infos) > MAX_ZIP_UNCOMPRESSED:
                _fail("inspection_limit_exceeded", "OOXML archive exceeds bounded inspection limits.")
            if len(names) != len(set(names)) or any(not _member_path(name) for name in names):
                _fail("unsafe_zip_members", "Archive has duplicate or unsafe member paths.")
            if any(stat.S_ISLNK(i.external_attr >> 16) or i.flag_bits & 1 for i in infos):
                _fail("unsafe_zip_members", "Symlink or encrypted archive members are not accepted.")
            required = {"[Content_Types].xml", "_rels/.rels", main}
            if not required.issubset(names):
                _fail("wrong_ooxml_type", "Required OOXML members for this extension are missing.")

            def xml_member(name):
                if archive.getinfo(name).file_size > MAX_XML_MEMBER_BYTES:
                    _fail("inspection_limit_exceeded", "An OOXML XML member exceeds inspection limits.")
                return _xml(archive.read(name))

            types = xml_member("[Content_Types].xml")
            ct_ns = "{http://schemas.openxmlformats.org/package/2006/content-types}"
            if types.tag != ct_ns + "Types" or not any(v.get("PartName") == "/" + main and v.get("ContentType") == content_type for v in types.findall(ct_ns + "Override")):
                _fail("wrong_ooxml_type", "OOXML main-part content type does not match the file extension.")
            rels = xml_member("_rels/.rels")
            rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
            office_rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
            if rels.tag != rel_ns + "Relationships" or not any(r.get("Type") == office_rel and r.get("Target", "").lstrip("/") == main and r.get("TargetMode") != "External" for r in rels.findall(rel_ns + "Relationship")):
                _fail("wrong_ooxml_type", "OOXML package relationship does not point to the expected main part.")
            root = xml_member(main)
            if root.tag != "{" + namespace + "}" + local_root:
                _fail("wrong_ooxml_type", "OOXML main XML root does not match the declared format.")
            if suffix == ".docx" and root.find("{" + namespace + "}body") is None:
                _fail("invalid_ooxml", "Word document is missing its body element.")
            for name in names:
                if name.endswith((".xml", ".rels")) and name not in required:
                    xml_member(name)
            # CRC test decompresses within the total-size bound; nothing is extracted.
            if archive.testzip() is not None:
                _fail("invalid_ooxml", "OOXML archive checksum verification failed.")
            return {"package_type": suffix[1:], "members": len(names),
                    "check_scope": "ZIP integrity, expected main part/content type/relationship and XML well-formedness; not complete Office validation or rendering."}
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError, NotImplementedError, KeyError, EOFError):
        _fail("invalid_ooxml", "OOXML ZIP structure or compression is invalid or unsupported.")


def _ics(data):
    lines = _text(data).replace("\r\n", "\n").splitlines()
    unfolded = []
    for line in lines:
        if line.startswith((" ", "\t")) and unfolded:
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)
    if not unfolded or unfolded[0] != "BEGIN:VCALENDAR" or unfolded[-1] != "END:VCALENDAR" or "VERSION:2.0" not in unfolded:
        _fail("invalid_ics", "Calendar needs a VCALENDAR envelope and VERSION:2.0.")
    stack = []
    for line in unfolded:
        if line.startswith("BEGIN:"):
            stack.append(line[6:])
        elif line.startswith("END:"):
            if not stack or stack.pop() != line[4:]:
                _fail("invalid_ics", "Calendar component delimiters do not match.")
    if stack:
        _fail("invalid_ics", "Calendar component is not closed.")
    return {"check_scope": "Calendar envelope/component balance only; not event dates, timezone or calendar-app import."}


SUPPORTED = {".json", ".geojson", ".csv", ".tsv", ".xml", ".svg", ".graphml", ".html", ".htm", ".pdf", ".md", ".txt", ".ics"} | set(OOXML)


def check_structure(data, suffix):
    if suffix in OOXML:
        return _ooxml(data, suffix)
    if suffix == ".json":
        _json(data)
        return {"check_scope": "Strict JSON syntax, unique object keys and standard numeric constants only."}
    if suffix == ".geojson":
        return _geojson(_json(data))
    if suffix in (".csv", ".tsv"):
        return _csv(data, "\t" if suffix == ".tsv" else ",")
    if suffix in (".xml", ".svg", ".graphml"):
        root = _xml(data)
        if suffix == ".svg" and root.tag not in ("svg", "{http://www.w3.org/2000/svg}svg"):
            _fail("invalid_svg", "SVG needs an svg root element.")
        if suffix == ".graphml":
            return _graphml(root)
        return {"check_scope": "Well-formed XML and, for SVG, the root element only; not rendering or external-resource safety."}
    if suffix in (".html", ".htm"):
        return _html(data)
    if suffix == ".pdf":
        if not re.match(br"%PDF-(?:1\.[0-7]|2\.0)(?:\r|\n)", data) or b"%%EOF" not in data[-1024:]:
            _fail("invalid_pdf_signature", "PDF header or final EOF marker is missing.")
        return {"check_scope": "PDF header and final EOF markers only; not PDF object integrity, page count, encryption or rendering."}
    if suffix in (".md", ".txt"):
        if not _text(data).strip():
            _fail("blank_text", "Text artifact contains no non-whitespace text.")
        return {"check_scope": "Nonblank UTF-8 text only; not Markdown semantics or useful content."}
    if suffix == ".ics":
        return _ics(data)
    _fail("unsupported_format", "No structural checker is available for this file extension.")


def _artifact_names(spec):
    if not isinstance(spec, dict) or not isinstance(spec.get("artifact_files"), list) or not spec["artifact_files"]:
        _fail("invalid_spec", "Spec needs a nonempty artifact_files array of relative-path strings.")
    names = spec["artifact_files"]
    for name in names:
        if not isinstance(name, str) or not name or "\\" in name or ":" in name or name.startswith("/") or any(ord(c) < 32 for c in name):
            _fail("unsafe_artifact_path", "Artifact names must be safe relative paths.")
        if any(part in ("", ".", "..") for part in name.split("/")) or any(c in name for c in "*?[]"):
            _fail("unsafe_artifact_path", "Artifact names must be literal paths without traversal or globs.")
    if len(names) != len(set(names)):
        _fail("invalid_spec", "Artifact paths must be unique.")
    return names


def verify_artifacts(directory, spec, output_path=None):
    names = _artifact_names(spec)
    absolute, parts = _absolute_parts(directory)
    directory_fd = _directory_fd(parts)
    os.close(directory_fd)
    if output_path is not None:
        report_path = _absolute_parts(output_path)[0]
        if report_path in {os.path.join(absolute, name) for name in names}:
            _fail("output_is_artifact", "Audit output must not be one of the required artifact files.")
    records = []
    for name in names:
        entry = {"artifact": name, "present": False, "nonempty": False, "bytes": None,
                 "structurally_checked": False, "structurally_valid": None, "status": "missing"}
        path = os.path.join(absolute, name)
        try:
            with _open_file(path) as stream:
                size = os.fstat(stream.fileno()).st_size
            entry.update(present=True, nonempty=size > 0, bytes=size)
            if not size:
                entry.update(status="empty", error_code="empty_file")
            else:
                suffix = PurePosixPath(name).suffix.lower()
                if suffix not in SUPPORTED:
                    entry.update(status="present_unchecked", error_code="unsupported_format")
                else:
                    data = _read_file(path, MAX_PARSE_BYTES)
                    entry["structurally_checked"] = True
                    entry["details"] = check_structure(data, suffix)
                    entry.update(structurally_valid=True, status="structure_passed")
        except AuditError as exc:
            entry["error_code"] = exc.code
            if entry["structurally_checked"]:
                entry["structurally_valid"] = False
            entry["status"] = "missing" if exc.code == "file_missing" else "rejected"
        records.append(entry)
    counts = {"required": len(records), "present": sum(r["present"] for r in records),
              "nonempty": sum(r["nonempty"] for r in records),
              "structurally_checked": sum(r["structurally_checked"] for r in records),
              "structure_passed": sum(r["structurally_valid"] is True for r in records)}
    passed = counts["structure_passed"] == counts["required"]
    return {"schema_version": SCHEMA_VERSION, "kind": "artifact_structure_audit", "ok": passed,
            "result": "mechanical_checks_passed" if passed else "failed_or_incomplete",
            "counts": counts, "artifacts": records, "limitation": LIMITATION,
            "inspection_limits": {"max_parse_bytes": MAX_PARSE_BYTES, "max_zip_members": MAX_ZIP_MEMBERS,
                                  "max_zip_uncompressed_bytes": MAX_ZIP_UNCOMPRESSED}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    sources = commands.add_parser("sources", help="Fingerprint only explicitly supplied local files.")
    sources.add_argument("--input", action="append", required=True, metavar="FILE")
    sources.add_argument("--output", required=True)
    verify = commands.add_parser("verify", help="Check literal artifact_files paths from a JSON spec.")
    verify.add_argument("--directory", required=True)
    verify.add_argument("--spec", required=True)
    verify.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        _output_available(args.output)
        if args.command == "sources":
            report = source_manifest(args.input)
            code = 0
        else:
            spec = _json(_read_file(args.spec, MAX_SPEC_BYTES))
            report = verify_artifacts(args.directory, spec, args.output)
            code = 0 if report["ok"] else 1
        _write_json_exclusive(args.output, report)
        print(json.dumps({"result": "source_fingerprints_written" if args.command == "sources" else report["result"],
                          "exit_code": code}, ensure_ascii=False))
        return code
    except AuditError as exc:
        print(json.dumps({"error": exc.code, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (OSError, ValueError, RecursionError):
        print(json.dumps({"error": "local_processing_error", "message": "Local processing failed; no raw file paths or content are disclosed."}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
