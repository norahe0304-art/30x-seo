#!/usr/bin/env python3
"""
Health check for 30x SEO installation.

Validates Python dependencies, API credentials, skill integrity,
and agent configuration.

Usage:
    python health_check.py
    python health_check.py --json
    python health_check.py --fix
"""

import argparse
import importlib
import json
import re
import sys
from pathlib import Path


def find_project_root() -> Path:
    """Find the 30x-seo project root."""
    # Try common locations
    candidates = [
        Path(__file__).parent.parent,  # scripts/ -> root
        Path.cwd(),
        Path.home() / "30x-seo",
    ]
    for p in candidates:
        if (p / "seo" / "SKILL.md").exists() or (p / "skills").is_dir():
            return p
    return candidates[0]


def check_python_deps() -> list[dict]:
    """Check Python dependencies are installed."""
    results = []
    deps = {
        "beautifulsoup4": "bs4",
        "requests": "requests",
        "lxml": "lxml",
        "Pillow": "PIL",
        "urllib3": "urllib3",
        "validators": "validators",
    }
    optional_deps = {
        "playwright": "playwright",
    }

    for pkg_name, import_name in deps.items():
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "unknown")
            results.append({
                "check": f"Python: {pkg_name}",
                "status": "pass",
                "detail": f"v{version}",
            })
        except ImportError:
            results.append({
                "check": f"Python: {pkg_name}",
                "status": "fail",
                "detail": "Not installed",
                "fix": f"pip install {pkg_name}",
            })

    for pkg_name, import_name in optional_deps.items():
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "unknown")
            results.append({
                "check": f"Python (optional): {pkg_name}",
                "status": "pass",
                "detail": f"v{version}",
            })
        except ImportError:
            results.append({
                "check": f"Python (optional): {pkg_name}",
                "status": "skip",
                "detail": "Not installed (optional — needed for screenshots only)",
            })

    return results


def check_credentials() -> list[dict]:
    """Check API credentials are configured."""
    results = []

    # DataForSEO
    auth_path = Path.home() / ".config" / "dataforseo" / "auth"
    if auth_path.exists():
        content = auth_path.read_text().strip()
        if len(content) > 10:
            results.append({
                "check": "DataForSEO credentials",
                "status": "pass",
                "detail": f"Found at {auth_path}",
            })
        else:
            results.append({
                "check": "DataForSEO credentials",
                "status": "warn",
                "detail": "File exists but seems empty/short",
            })
    else:
        results.append({
            "check": "DataForSEO credentials",
            "status": "skip",
            "detail": "Not configured (needed for keywords, backlinks, SERP, AI visibility)",
            "fix": (
                f"mkdir -p {auth_path.parent} && "
                f"echo -n 'login:password' | base64 > {auth_path}"
            ),
        })

    # Google API key
    google_key_path = Path.home() / ".config" / "google" / "api_key"
    if google_key_path.exists():
        results.append({
            "check": "Google API key",
            "status": "pass",
            "detail": f"Found at {google_key_path}",
        })
    else:
        results.append({
            "check": "Google API key",
            "status": "skip",
            "detail": "Not configured (needed for CrUX/PageSpeed Insights)",
        })

    return results


def check_skills(root: Path) -> list[dict]:
    """Validate skill directory integrity."""
    results = []
    skills_dir = root / "skills"

    if not skills_dir.is_dir():
        results.append({
            "check": "Skills directory",
            "status": "fail",
            "detail": f"Not found at {skills_dir}",
        })
        return results

    skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir()])
    valid_count = 0
    issues = []

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            issues.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        content = skill_md.read_text()

        # Check YAML frontmatter
        if not content.startswith("---"):
            issues.append(f"{skill_dir.name}: missing YAML frontmatter")
            continue

        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append(f"{skill_dir.name}: malformed YAML frontmatter")
            continue

        frontmatter = parts[1]
        if "name:" not in frontmatter:
            issues.append(f"{skill_dir.name}: missing 'name' in frontmatter")
        elif "description:" not in frontmatter:
            issues.append(f"{skill_dir.name}: missing 'description' in frontmatter")
        else:
            valid_count += 1

    results.append({
        "check": "Skills integrity",
        "status": "pass" if not issues else "warn",
        "detail": f"{valid_count}/{len(skill_dirs)} skills valid",
        "issues": issues if issues else None,
    })

    return results


def check_agents(root: Path) -> list[dict]:
    """Validate agent files."""
    results = []
    agents_dir = root / "agents"

    if not agents_dir.is_dir():
        results.append({
            "check": "Agents directory",
            "status": "fail",
            "detail": f"Not found at {agents_dir}",
        })
        return results

    agent_files = sorted(agents_dir.glob("*.md"))
    valid_count = 0
    issues = []

    for agent_file in agent_files:
        content = agent_file.read_text()

        if not content.startswith("---"):
            issues.append(f"{agent_file.name}: missing YAML frontmatter")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append(f"{agent_file.name}: malformed frontmatter")
            continue

        frontmatter = parts[1]
        missing = []
        for field in ["name:", "description:", "tools:"]:
            if field not in frontmatter:
                missing.append(field.rstrip(":"))
        if missing:
            issues.append(f"{agent_file.name}: missing fields: {', '.join(missing)}")
        else:
            valid_count += 1

    results.append({
        "check": "Agents integrity",
        "status": "pass" if not issues else "warn",
        "detail": f"{valid_count}/{len(agent_files)} agents valid",
        "issues": issues if issues else None,
    })

    return results


def check_routing(root: Path) -> list[dict]:
    """Validate orchestrator routing table matches skill directories."""
    results = []
    orchestrator = root / "seo" / "SKILL.md"

    if not orchestrator.exists():
        results.append({
            "check": "Orchestrator routing",
            "status": "fail",
            "detail": "seo/SKILL.md not found",
        })
        return results

    content = orchestrator.read_text()

    # Extract routing entries: | `command` | 30x-seo-skillname |
    routes = re.findall(r"\|\s*`(\w[\w-]*)`\s*\|\s*(30x-seo-[\w-]+)\s*\|", content)

    skills_dir = root / "skills"
    existing_skills = (
        {d.name for d in skills_dir.iterdir() if d.is_dir()}
        if skills_dir.is_dir()
        else set()
    )

    missing_dirs = []
    for cmd, skill_name in routes:
        if skill_name not in existing_skills:
            missing_dirs.append(f"Route '{cmd}' → {skill_name} (directory missing)")

    unrouted = existing_skills - {skill for _, skill in routes} - {"30x-seo"}
    unrouted_list = [f"{s} (no route in orchestrator)" for s in sorted(unrouted)]

    issues = missing_dirs + unrouted_list

    results.append({
        "check": "Routing table",
        "status": "pass" if not issues else "warn",
        "detail": f"{len(routes)} routes, {len(existing_skills) - 1} skills",
        "issues": issues if issues else None,
    })

    return results


def check_scripts(root: Path) -> list[dict]:
    """Check Python scripts have valid syntax."""
    results = []
    scripts_dir = root / "scripts"

    if not scripts_dir.is_dir():
        return results

    scripts = sorted(scripts_dir.glob("*.py"))
    valid = 0
    issues = []

    for script in scripts:
        try:
            compile(script.read_text(), str(script), "exec")
            valid += 1
        except SyntaxError as e:
            issues.append(f"{script.name}: syntax error at line {e.lineno}")

    results.append({
        "check": "Script syntax",
        "status": "pass" if not issues else "fail",
        "detail": f"{valid}/{len(scripts)} scripts valid",
        "issues": issues if issues else None,
    })

    return results


def run_health_check(root: Path) -> dict:
    """Run all health checks."""
    all_results = []
    all_results.extend(check_python_deps())
    all_results.extend(check_credentials())
    all_results.extend(check_skills(root))
    all_results.extend(check_agents(root))
    all_results.extend(check_routing(root))
    all_results.extend(check_scripts(root))

    pass_count = sum(1 for r in all_results if r["status"] == "pass")
    fail_count = sum(1 for r in all_results if r["status"] == "fail")
    warn_count = sum(1 for r in all_results if r["status"] == "warn")
    skip_count = sum(1 for r in all_results if r["status"] == "skip")

    return {
        "project_root": str(root),
        "summary": {
            "total": len(all_results),
            "pass": pass_count,
            "fail": fail_count,
            "warn": warn_count,
            "skip": skip_count,
            "healthy": fail_count == 0,
        },
        "checks": all_results,
    }


def print_report(report: dict):
    """Print human-readable health check report."""
    summary = report["summary"]

    print("30x SEO Health Check")
    print("=" * 50)
    print(f"Project: {report['project_root']}")
    print()

    status_icons = {"pass": "✅", "fail": "❌", "warn": "⚠️", "skip": "⏭️"}

    for check in report["checks"]:
        icon = status_icons.get(check["status"], "?")
        print(f"  {icon} {check['check']}: {check['detail']}")
        if check.get("fix"):
            print(f"     Fix: {check['fix']}")
        if check.get("issues"):
            for issue in check["issues"]:
                print(f"     - {issue}")

    print()
    print(f"Results: {summary['pass']} pass, {summary['fail']} fail, "
          f"{summary['warn']} warn, {summary['skip']} skip")

    if summary["healthy"]:
        print("\n✅ Installation is healthy!")
    else:
        print(f"\n❌ {summary['fail']} issue(s) need attention.")


def main():
    parser = argparse.ArgumentParser(description="30x SEO health check")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--root", help="Project root directory")

    args = parser.parse_args()

    root = Path(args.root) if args.root else find_project_root()
    report = run_health_check(root)

    if args.json:
        # Clean None values from issues
        for check in report["checks"]:
            if check.get("issues") is None:
                del check["issues"]
            if check.get("fix") is None and "fix" in check:
                del check["fix"]
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

    sys.exit(0 if report["summary"]["healthy"] else 1)


if __name__ == "__main__":
    main()
