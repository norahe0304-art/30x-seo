# TODO — 30x SEO

## Completed in v1.2.0

- [x] **Fix YAML frontmatter parsing** — Removed HTML comments before `---` in 8 files (from @kylewhirl fork)
- [x] **SSRF prevention in Python scripts** — Private IP blocking in fetch_page.py and analyze_visual.py (from @artyomsv #7)
- [x] **Install hardening** — venv-based pip, no `--break-system-packages` (from @JawandS #2)
- [x] **Windows install fixes** — `python -m pip`, `py -3` fallback, requirements.txt persistence (from @kfrancis #5, PR #6)
- [x] **requirements.txt persistence** — Copied to skill dir after install (from @edustef #1)
- [x] **Path traversal prevention** — Output path sanitization in capture_screenshot.py, file validation in parse_html.py

## Deferred from Community Feedback

- [ ] **Reduce Bash scope on agents** (Priority: Medium, from @artyomsv #7)
  Evaluate which agents truly need Bash access. Consider replacing with WebFetch where possible.

- [ ] **Docker-based script execution** (Priority: Low, from @artyomsv #7)
  Sandbox Python scripts in Docker for users who want extra isolation.

- [ ] **Opencode compatibility** (Priority: Low, from @Ehtz #4)
  Adapt skill architecture for Opencode. @kylewhirl already ported to OpenAI Codex.

- [ ] **Subagent timeout/compact handling** (Priority: Medium, from @JawandS #3)
  Primary agent sometimes terminates before subagents finish. Consider encouraging subagents
  to run /compact and adding explicit wait logic.

- [ ] **Native Chrome tools vs Playwright** (Priority: Medium, from @artyomsv #7, @btafoya PR #8)
  Claude Code has native browser automation. Evaluate replacing Playwright with built-in tools
  to eliminate the ~200MB Chromium dependency.

## Deferred from February 2026 Research Report

- [ ] **Fake freshness detection** (Priority: Medium)
  Compare visible dates (`datePublished`, `dateModified`) against actual content modification signals.
  Flag pages with updated dates but unchanged body content.

- [ ] **Mobile content parity check** (Priority: Medium)
  Compare mobile vs desktop meta tags, structured data presence, and content completeness.
  Flag discrepancies that could affect mobile-first indexing.

- [ ] **Discover optimization checks** (Priority: Low-Medium)
  Clickbait title detection, content depth scoring, local relevance signals, sensationalism flags.

- [ ] **Brand mention analysis Python implementation** (Priority: Low)
  Currently documented in `seo-geo/SKILL.md` but no programmatic scoring.

---

*Last updated: February 19, 2026*
