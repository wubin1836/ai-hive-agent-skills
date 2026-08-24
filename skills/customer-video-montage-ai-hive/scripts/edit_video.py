#!/usr/bin/env python3
"""Small, auditable ffmpeg helper for deterministic short-video edits."""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Missing {name}. Install ffmpeg first.")
    return path


def run(args: list[str]) -> None:
    print(" ".join(args))
    subprocess.run(args, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic short-video editing helper")
    sub = parser.add_subparsers(dest="command", required=True)

    probe = sub.add_parser("probe")
    probe.add_argument("--input", required=True)

    trim = sub.add_parser("trim")
    trim.add_argument("--input", required=True)
    trim.add_argument("--output", required=True)
    trim.add_argument("--start", required=True)
    trim.add_argument("--duration", required=True)

    aspect = sub.add_parser("aspect")
    aspect.add_argument("--input", required=True)
    aspect.add_argument("--output", required=True)
    aspect.add_argument("--ratio", choices=["9:16", "16:9", "1:1", "4:5"], required=True)
    aspect.add_argument("--mode", choices=["crop", "pad"], default="pad")

    mute = sub.add_parser("mute")
    mute.add_argument("--input", required=True)
    mute.add_argument("--output", required=True)

    loudnorm = sub.add_parser("loudnorm")
    loudnorm.add_argument("--input", required=True)
    loudnorm.add_argument("--output", required=True)

    concat = sub.add_parser("concat")
    concat.add_argument("--input", action="append", required=True)
    concat.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "probe":
        run([binary("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(Path(args.input).expanduser())])
        return

    ffmpeg = binary("ffmpeg")
    source = str(Path(args.input).expanduser()) if hasattr(args, "input") and isinstance(args.input, str) else ""
    output = str(Path(args.output).expanduser())
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    if args.command == "trim":
        run([ffmpeg, "-y", "-ss", args.start, "-i", source, "-t", args.duration, "-c:v", "libx264", "-c:a", "aac", output])
    elif args.command == "aspect":
        dims = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
        width, height = dims[args.ratio]
        if args.mode == "crop":
            vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
        else:
            vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"
        run([ffmpeg, "-y", "-i", source, "-vf", vf, "-c:v", "libx264", "-c:a", "aac", output])
    elif args.command == "mute":
        run([ffmpeg, "-y", "-i", source, "-c:v", "copy", "-an", output])
    elif args.command == "loudnorm":
        run([ffmpeg, "-y", "-i", source, "-af", "loudnorm=I=-16:LRA=11:TP=-1.5", "-c:v", "copy", "-c:a", "aac", output])
    elif args.command == "concat":
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as handle:
            for item in args.input:
                safe = str(Path(item).expanduser().resolve()).replace("'", "'\\''")
                handle.write(f"file '{safe}'\n")
            list_path = handle.name
        try:
            run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", list_path, "-c", "copy", output])
        finally:
            Path(list_path).unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"ffmpeg failed with exit code {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode)
