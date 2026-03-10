#!/usr/bin/env python3
"""Validate that all skills and agents have proper metadata.

Checks performed:
1. Every directory in skills/ has a SKILL.md
2. Every SKILL.md has valid YAML frontmatter with 'name' and 'description'
3. Every agent in agents/ has valid YAML frontmatter with 'name', 'description', 'tools'
4. The orchestrator routing table in seo/SKILL.md has entries for all skill directories
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
AGENTS_DIR = REPO_ROOT / "agents"
ORCHESTRATOR = REPO_ROOT / "seo" / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)

errors: list[str] = []


def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{filepath}: invalid YAML frontmatter: {exc}")
        return None


def validate_skills() -> None:
    """Check that every skill directory has a valid SKILL.md."""
    if not SKILLS_DIR.is_dir():
        errors.append(f"skills/ directory not found at {SKILLS_DIR}")
        return

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        meta = parse_frontmatter(skill_md)
        if meta is None:
            errors.append(f"{skill_dir.name}/SKILL.md: missing YAML frontmatter")
            continue

        for field in ("name", "description"):
            if field not in meta:
                errors.append(
                    f"{skill_dir.name}/SKILL.md: frontmatter missing '{field}'"
                )


def validate_agents() -> None:
    """Check that every agent definition has required frontmatter fields."""
    if not AGENTS_DIR.is_dir():
        errors.append(f"agents/ directory not found at {AGENTS_DIR}")
        return

    for agent_file in sorted(AGENTS_DIR.glob("*.md")):
        meta = parse_frontmatter(agent_file)
        if meta is None:
            errors.append(f"agents/{agent_file.name}: missing YAML frontmatter")
            continue

        for field in ("name", "description", "tools"):
            if field not in meta:
                errors.append(
                    f"agents/{agent_file.name}: frontmatter missing '{field}'"
                )


def validate_routing_table() -> None:
    """Check that the orchestrator routing table covers all skill directories."""
    if not ORCHESTRATOR.exists():
        errors.append(f"Orchestrator SKILL.md not found at {ORCHESTRATOR}")
        return

    orchestrator_text = ORCHESTRATOR.read_text(encoding="utf-8")

    # Extract skill names referenced in the routing table
    # Pattern matches lines like: | `page` | 30x-seo-page |
    routing_re = re.compile(r"\|\s*`[^`]+`\s*\|\s*(30x-seo-[\w-]+)\s*\|")
    routed_skills = set(routing_re.findall(orchestrator_text))

    if not SKILLS_DIR.is_dir():
        return

    skill_dirs = {
        d.name for d in SKILLS_DIR.iterdir() if d.is_dir()
    }

    missing = skill_dirs - routed_skills
    if missing:
        for name in sorted(missing):
            errors.append(
                f"Skill '{name}' exists in skills/ but has no entry in the "
                f"orchestrator routing table (seo/SKILL.md)"
            )


def main() -> int:
    print("Validating skills and agents...")
    print()

    validate_skills()
    validate_agents()
    validate_routing_table()

    if errors:
        print(f"FAILED: {len(errors)} error(s) found:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    # Print summary
    skill_count = sum(1 for d in SKILLS_DIR.iterdir() if d.is_dir())
    agent_count = sum(1 for _ in AGENTS_DIR.glob("*.md"))
    print(f"OK: {skill_count} skills, {agent_count} agents validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
