"""Validate repository skill metadata and local Markdown references."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = "learn-architecture-by-mini"


def validate(root: Path) -> list[str]:
    errors = []
    for path in ("SKILL.md", "README.md", "agents/openai.yaml", "references/blueprint.md"):
        if not (root / path).is_file():
            errors.append(f"Missing required file: {path}")
    if errors:
        return errors
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
    if not match:
        errors.append("SKILL.md must start with YAML frontmatter")
    else:
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict) or set(metadata) != {"name", "description"}:
            errors.append("Frontmatter must contain exactly name and description")
        else:
            if metadata["name"] != NAME:
                errors.append(f"Skill name must be {NAME}")
            desc = metadata["description"]
            if not isinstance(desc, str) or not desc.strip():
                errors.append("Skill description must be nonempty text")
    if len(skill.splitlines()) >= 500:
        errors.append("Keep SKILL.md below 500 lines")
    config = yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))
    interface = config.get("interface", {}) if isinstance(config, dict) else {}
    for field in ("display_name", "short_description", "default_prompt"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Missing interface.{field}")
    short = interface.get("short_description", "")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        errors.append("short_description must contain 25–64 characters")
    prompt = interface.get("default_prompt", "")
    if not isinstance(prompt, str) or f"${NAME}" not in prompt:
        errors.append("default_prompt must mention the skill by $name")
    for md in root.rglob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).is_file():
                errors.append(f"Broken link in {md.relative_to(root)}: {target}")
    return errors


if __name__ == "__main__":
    try:
        errors = validate(ROOT)
    except (OSError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        sys.exit(1)
    print("Skill metadata and local references are valid.")
