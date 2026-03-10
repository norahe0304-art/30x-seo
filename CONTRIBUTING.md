# Contributing to 30x SEO

## Getting Started

```bash
git clone https://github.com/norahe0304-art/30x-seo.git
cd 30x-seo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional: screenshots require Playwright + Chromium
pip install -r requirements-optional.txt
playwright install chromium
```

Install the skill in Claude Code by adding the project directory to your Claude Code configuration. Skills are discovered automatically from `seo/SKILL.md`.

---

## Project Structure

```
30x-seo/
├── seo/SKILL.md               # Main orchestrator (routing table lives here)
├── seo/references/             # On-demand reference files (schema-types, CWV, etc.)
├── skills/30x-seo-{name}/     # Sub-skills (one SKILL.md per directory)
├── agents/seo-{name}.md       # Subagents for parallel audit execution
├── scripts/                   # Python utilities (fetch, parse, analyze)
├── hooks/                     # Pre/post edit hooks
├── schema/                    # Schema.org templates
├── docs/                      # Architecture, installation, troubleshooting
├── requirements.txt           # Core Python deps
├── requirements-optional.txt  # Playwright (optional)
└── CHANGELOG.md               # Keep a Changelog format
```

---

## Adding a New Skill

### 1. Create the skill directory and SKILL.md

```bash
mkdir skills/30x-seo-myskill
```

Create `skills/30x-seo-myskill/SKILL.md` with this structure:

```yaml
---
# REQUIRED: must match the directory name
name: 30x-seo-myskill
# REQUIRED: describe WHEN to invoke this skill.
# Include trigger keywords the orchestrator uses for routing.
description: >
  One-paragraph description of what this skill does and when to use it.
  Triggers on: "keyword1", "keyword2", "keyword3".
# REQUIRED: list only the tools this skill actually needs.
# Prefer WebFetch over Bash for HTTP operations.
allowed-tools:
  - WebFetch
  - Read
---

# Skill Title

## What to Analyze
<!-- Step-by-step instructions for the agent executing this skill -->

## Output
<!-- Define the expected output format: tables, scores, JSON-LD, etc. -->
```

Key rules for SKILL.md:
- `description` must contain trigger keywords so the orchestrator can route to it.
- Keep the file under 200 lines. Move static data to a `references/` subdirectory.
- Never recommend deprecated schema types (HowTo, SpecialAnnouncement, CourseInfo).
- All Core Web Vitals references must use INP, never FID.

### 2. Update the orchestrator routing table

Edit `seo/SKILL.md` and add your skill in two places:

**Quick Reference table** (under the appropriate category heading):
```markdown
| `/seo myskill <url>` | What it does in one line |
```

**Command -> Skill Routing table**:
```markdown
| `myskill` | 30x-seo-myskill |
```

### 3. Add reference files (if needed)

If your skill needs static lookup data (thresholds, templates, type lists), create `skills/30x-seo-myskill/references/` and load files on-demand from the skill instructions rather than inlining them.

### 4. Add tests

Verify your skill manually:
- Invoke it via `/seo myskill <url>` with a real URL.
- Confirm the output matches the format defined in your SKILL.md.
- Test edge cases: missing data, non-HTML responses, redirected URLs.

---

## Adding a New Subagent

Subagents run in parallel during `/seo audit`. They are specialized workers with constrained tool access.

### 1. Create the agent file

Create `agents/seo-myagent.md`:

```yaml
---
# REQUIRED
name: seo-myagent
# REQUIRED: one-line description
description: What this agent specializes in.
# REQUIRED: comma-separated tool list.
# Prefer WebFetch over Bash for all HTTP operations.
# Only seo-performance and seo-visual should have Bash access.
tools: Read, WebFetch, Write
---

You are a [domain] specialist.

Use WebFetch to retrieve page HTML for analysis. Do NOT use Bash for page fetching.

## Instructions
<!-- What this agent should do when invoked -->

## Output Format
<!-- What to return to the orchestrator -->
```

### 2. Tool selection guidance

| Need | Use | Do NOT use |
|------|-----|------------|
| Fetch a web page | `WebFetch` | `Bash` with curl/wget |
| Read local files | `Read` | `Bash` with cat |
| Search codebase | `Grep`, `Glob` | `Bash` with find/grep |
| Run Python scripts | `Bash` | -- |
| Take screenshots | `Bash` (Playwright) | -- |

Only grant `Bash` to agents that genuinely need it (script execution, screenshot capture).

### 3. Reference from skills

If your subagent should be spawned during audits, add it to the orchestrator's subagent list in `seo/SKILL.md` under the **Orchestration Logic** and **Subagents** sections.

---

## Adding a Python Script

Scripts live in `scripts/` and follow this pattern: `{action}_{target}.py` (e.g., `fetch_page.py`, `analyze_visual.py`).

### Required patterns

**SSRF prevention** -- mandatory for any script that fetches URLs:

```python
import ipaddress
import socket
from urllib.parse import urlparse

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    try:
        ip = socket.getaddrinfo(parsed.hostname, None)[0][4][0]
        addr = ipaddress.ip_address(ip)
        if addr.is_private or addr.is_loopback or addr.is_reserved:
            return False
    except (socket.gaierror, ValueError):
        return False
    return True
```

**Path traversal prevention** -- mandatory for any script that writes files:

```python
import os

def safe_output_path(user_path: str, allowed_dir: str) -> str:
    resolved = os.path.realpath(os.path.join(allowed_dir, user_path))
    if not resolved.startswith(os.path.realpath(allowed_dir)):
        raise ValueError(f"Path traversal blocked: {user_path}")
    return resolved
```

**CLI interface** -- use argparse with a `--json` output mode:

```python
import argparse
import json

parser = argparse.ArgumentParser(description="What this script does")
parser.add_argument("url", help="Target URL")
parser.add_argument("--output", help="Output file path")
parser.add_argument("--json", action="store_true", help="Output as JSON")
args = parser.parse_args()
```

**Dependencies** -- only use packages already in `requirements.txt`. If you need a new dependency, add it with bounded version pinning (`>=x.y.z,<next_major`) and note any known CVEs.

---

## Quality Checklist

Before submitting, verify:

- [ ] SKILL.md has valid YAML frontmatter (name, description, allowed-tools)
- [ ] Description includes trigger keywords for orchestrator routing
- [ ] No deprecated schema types recommended (HowTo, SpecialAnnouncement, CourseInfo)
- [ ] All CWV references use INP, never FID
- [ ] FAQ schema only recommended for government/healthcare sites
- [ ] Tests pass (manual invocation with real URLs)
- [ ] Routing table updated in `seo/SKILL.md` (both Quick Reference and Routing sections)
- [ ] CHANGELOG.md updated with the change under an `[Unreleased]` heading
- [ ] Python scripts include SSRF prevention for URL fetching
- [ ] Python scripts include path traversal prevention for file output
- [ ] Skill file is under 200 lines (static data moved to `references/`)

---

## Code Style

**Python:**
- Formatter/linter: ruff with default settings
- No type stubs required
- Use `argparse` for all CLI scripts
- Version-pin dependencies with bounds: `>=x.y.z,<next_major`
- Graceful import failures (see `fetch_page.py` for pattern)

**Markdown (Skills/Agents):**
- YAML frontmatter delimited by `---`
- One H1 heading per file
- Tables for structured output formats
- Keep instructions imperative ("Check X", "Flag Y"), not narrative

---

## PR Process

### Branch naming

```
feat/30x-seo-{skillname}     # New skill
feat/seo-{agentname}         # New agent
fix/{short-description}      # Bug fix
docs/{short-description}     # Documentation
```

### Commit messages

Use conventional commits:

```
feat(skill): add 30x-seo-myskill for X analysis
fix(schema): remove deprecated HowTo recommendation
docs: update routing table for new skills
```

### What reviewers check

1. YAML frontmatter is valid and complete
2. Trigger keywords in description are specific enough to avoid false routing
3. No deprecated schema types or FID references
4. Python scripts have SSRF and path traversal guards
5. Routing table in `seo/SKILL.md` is updated
6. CHANGELOG.md has an entry
7. Skill stays under 200 lines; heavy data lives in `references/`
