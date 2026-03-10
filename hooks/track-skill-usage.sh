#!/usr/bin/env bash
# Post-tool-use hook to track skill invocations via telemetry.
#
# Hook configuration in ~/.claude/settings.json:
# {
#   "hooks": {
#     "PostToolUse": [
#       {
#         "matcher": "Skill",
#         "hooks": [
#           {
#             "type": "command",
#             "command": "./hooks/track-skill-usage.sh \"$SKILL_NAME\""
#           }
#         ]
#       }
#     ]
#   }
# }

SKILL_NAME="${1:-unknown}"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Only track seo-related skills
case "$SKILL_NAME" in
  seo*|30x-seo*)
    python3 "$SCRIPT_DIR/scripts/telemetry.py" record --skill "$SKILL_NAME" 2>/dev/null || true
    ;;
esac

exit 0
