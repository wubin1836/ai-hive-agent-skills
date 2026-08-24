#!/usr/bin/env python3
"""Regenerate the repository catalog while preserving existing classifications."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
JSON_PATH = ROOT / "skills.json"
MARKDOWN_PATH = ROOT / "SKILLS.md"


def title_from_skill(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else fallback


def infer_kind(name: str, text: str) -> str:
    value = f"{name} {text[:2400]}".lower()
    if any(word in value for word in ("video", "\u89c6\u9891", "tvc", "\u77ed\u5267", "\u6f2b\u5267")):
        return "video"
    if any(word in value for word in ("image", "\u56fe\u7247", "\u4e3b\u56fe", "\u6d77\u62a5", "poster")):
        return "image"
    if any(word in value for word in ("audio", "\u97f3\u9891", "\u97f3\u4e50")):
        return "audio"
    return "workflow"


def main() -> None:
    existing = {
        item["name"]: item
        for item in json.loads(JSON_PATH.read_text(encoding="utf-8"))
    }
    rows: list[dict] = []
    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        name = skill_dir.name
        text = skill_file.read_text(encoding="utf-8")
        item = dict(existing.get(name, {}))
        item["name"] = name
        item.setdefault("kind", infer_kind(name, text))
        if name.startswith("ai-model-expert-drama-"):
            item.setdefault("layer", "drama-search-matrix")
        elif name.startswith("ai-model-expert-"):
            item.setdefault("layer", "ai-model-expert")
        else:
            item.setdefault("layer", "general")
        item["display_name"] = title_from_skill(text, name)
        item["model_ids"] = sorted(set(re.findall(r"public_model_[A-Za-z0-9_]+", text)))
        rows.append(item)

    JSON_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# AI Hive \u5b8c\u6574 Skill \u76ee\u5f55",
        "",
        f"\u4ed3\u5e93\u5f53\u524d\u5305\u542b {len(rows)} \u4e2a\u53ef\u72ec\u7acb\u5b89\u88c5\u7684 Agent Skill\uff1a340 \u4e2a\u539f\u6709 Skill\u3001340 \u4e2a\u901a\u7528 AI\u5927\u6a21\u578b\u4e13\u5bb6 Skill\uff0c\u4ee5\u53ca 130 \u4e2a\u77ed\u5267\u6f2b\u5267\u3001\u526a\u8f91\u590d\u523b\u3001GEO/AEO \u548c API \u805a\u5408 Skill\u3002",
        "",
        "| Skill | \u5c55\u793a\u540d\u79f0 | \u7c7b\u578b | \u5c42\u7ea7 |",
        "|---|---|---|---|",
    ]
    for item in rows:
        name = item["name"]
        display = str(item.get("display_name") or name).replace("|", "\\|")
        lines.append(
            f"| [`{name}`](skills/{name}/SKILL.md) | {display} | {item.get('kind', '')} | {item.get('layer', '')} |"
        )
    MARKDOWN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"skills": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
