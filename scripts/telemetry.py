#!/usr/bin/env python3
"""
Optional anonymous telemetry for 30x SEO.

Tracks skill usage frequency and execution times locally.
Data stays on disk — nothing is sent externally.

Usage:
    # Record a skill invocation
    python telemetry.py record --skill seo-page --duration 3.2

    # View usage report
    python telemetry.py report

    # Export as JSON
    python telemetry.py report --json

    # Clear all data
    python telemetry.py clear

    # Disable telemetry
    python telemetry.py disable

    # Enable telemetry
    python telemetry.py enable
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

TELEMETRY_DIR = Path.home() / ".config" / "30x-seo"
TELEMETRY_FILE = TELEMETRY_DIR / "telemetry.jsonl"
DISABLED_FLAG = TELEMETRY_DIR / "telemetry-disabled"


def is_enabled() -> bool:
    """Check if telemetry is enabled."""
    return not DISABLED_FLAG.exists()


def record(skill: str, duration: float | None = None, success: bool = True):
    """Record a skill invocation."""
    if not is_enabled():
        return

    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "skill": skill,
        "success": success,
    }
    if duration is not None:
        entry["duration_s"] = round(duration, 2)

    with open(TELEMETRY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_entries() -> list[dict]:
    """Load all telemetry entries."""
    if not TELEMETRY_FILE.exists():
        return []

    entries = []
    for line in TELEMETRY_FILE.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def generate_report(as_json: bool = False) -> str:
    """Generate usage report."""
    entries = load_entries()

    if not entries:
        if as_json:
            return json.dumps({"total_invocations": 0, "skills": {}}, indent=2)
        return "No telemetry data recorded yet."

    # Aggregate by skill
    skills: dict[str, dict] = {}
    for entry in entries:
        name = entry["skill"]
        if name not in skills:
            skills[name] = {
                "count": 0,
                "success": 0,
                "fail": 0,
                "durations": [],
            }
        skills[name]["count"] += 1
        if entry.get("success", True):
            skills[name]["success"] += 1
        else:
            skills[name]["fail"] += 1
        if "duration_s" in entry:
            skills[name]["durations"].append(entry["duration_s"])

    # Build report
    total = len(entries)
    first_ts = entries[0].get("ts", "unknown")
    last_ts = entries[-1].get("ts", "unknown")

    if as_json:
        report_data = {
            "total_invocations": total,
            "period": {"first": first_ts, "last": last_ts},
            "skills": {},
        }
        for name, data in sorted(skills.items(), key=lambda x: x[1]["count"], reverse=True):
            avg_dur = (
                round(sum(data["durations"]) / len(data["durations"]), 2)
                if data["durations"]
                else None
            )
            report_data["skills"][name] = {
                "count": data["count"],
                "success": data["success"],
                "fail": data["fail"],
                "avg_duration_s": avg_dur,
            }
        return json.dumps(report_data, indent=2)

    lines = [
        "30x SEO Usage Report",
        "=" * 45,
        f"Total invocations: {total}",
        f"Period: {first_ts[:10]} to {last_ts[:10]}",
        "",
        f"{'Skill':<35} {'Count':<8} {'Avg Time':<10} {'Fail'}",
        f"{'-'*35} {'-'*8} {'-'*10} {'-'*5}",
    ]

    for name, data in sorted(skills.items(), key=lambda x: x[1]["count"], reverse=True):
        avg_dur = (
            f"{sum(data['durations']) / len(data['durations']):.1f}s"
            if data["durations"]
            else "—"
        )
        lines.append(f"{name:<35} {data['count']:<8} {avg_dur:<10} {data['fail']}")

    return "\n".join(lines)


def clear_data():
    """Clear all telemetry data."""
    if TELEMETRY_FILE.exists():
        TELEMETRY_FILE.unlink()
        print("Telemetry data cleared.")
    else:
        print("No telemetry data to clear.")


def disable():
    """Disable telemetry."""
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    DISABLED_FLAG.touch()
    print("Telemetry disabled. No data will be recorded.")
    print(f"To re-enable: rm {DISABLED_FLAG}")


def enable():
    """Enable telemetry."""
    if DISABLED_FLAG.exists():
        DISABLED_FLAG.unlink()
    print("Telemetry enabled. Data stored locally at:")
    print(f"  {TELEMETRY_FILE}")
    print("No data is sent externally.")


def main():
    parser = argparse.ArgumentParser(description="30x SEO anonymous telemetry (local only)")
    sub = parser.add_subparsers(dest="command")

    rec = sub.add_parser("record", help="Record a skill invocation")
    rec.add_argument("--skill", required=True, help="Skill name")
    rec.add_argument("--duration", type=float, help="Execution time in seconds")
    rec.add_argument("--fail", action="store_true", help="Mark as failed")

    rep = sub.add_parser("report", help="View usage report")
    rep.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    sub.add_parser("clear", help="Clear all telemetry data")
    sub.add_parser("disable", help="Disable telemetry")
    sub.add_parser("enable", help="Enable telemetry")
    sub.add_parser("status", help="Show telemetry status")

    args = parser.parse_args()

    if args.command == "record":
        record(args.skill, args.duration, success=not args.fail)
    elif args.command == "report":
        print(generate_report(as_json=args.json))
    elif args.command == "clear":
        clear_data()
    elif args.command == "disable":
        disable()
    elif args.command == "enable":
        enable()
    elif args.command == "status":
        status = "enabled" if is_enabled() else "disabled"
        entries = len(load_entries())
        print(f"Telemetry: {status}")
        print(f"Entries recorded: {entries}")
        print(f"Data file: {TELEMETRY_FILE}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
