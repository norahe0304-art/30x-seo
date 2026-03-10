# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-03-10

### Added
- **9 new skills** (32 total, 9 categories):
  - `30x-seo-fake-freshness`: Detect pages with updated dates but unchanged content. Scores authenticity 0-100.
  - `30x-seo-mobile-parity`: Compare mobile vs desktop content for mobile-first indexing parity.
  - `30x-seo-discover`: Google Discover optimization — clickbait detection, content depth, image readiness.
  - `30x-seo-rank-tracking`: Historical rank tracking, position change alerts, trending keywords (DataForSEO).
  - `30x-seo-competitive-tracking`: Competitor SERP monitoring, threat detection, new content alerts (DataForSEO).
  - `30x-seo-cwv-analytics`: CrUX field data, LCP subparts breakdown, INP diagnostics (Google API).
  - `30x-seo-semantic-search`: Entity extraction, topical authority scoring, Knowledge Panel eligibility.
  - `30x-seo-content-localization`: Translation quality, cultural adaptation, locale-specific keyword analysis.
  - `30x-seo-blog-pipeline`: End-to-end SEO blog production pipeline — keyword research, SERP analysis, outline, draft, optimization, CMS-ready output.
- **2 new Python scripts**:
  - `scripts/brand_mentions.py`: Brand mention extraction from AI responses with sentiment scoring and competitor comparison.
  - `scripts/health_check.py`: Installation health check — validates deps, credentials, skill integrity, routing table.
- **Testing infrastructure**:
  - pytest test suite with 257+ tests covering fetch_page, parse_html, brand_mentions, and skill routing validation.
  - `pytest.ini` configuration.
  - `requirements-dev.txt` with pytest + ruff.
- **CI/CD pipeline** (GitHub Actions):
  - `ci.yml`: Lint (ruff), test (pytest), validate skills (frontmatter + routing).
  - `release.yml`: Auto-release with Docker image builds on tag push.
  - Dependabot configuration for weekly dependency updates.
  - Issue templates for bug reports and feature requests.
- **Docker support**: `Dockerfile` (lightweight) and `Dockerfile.playwright` (with Chromium). Docs in `docs/DOCKER.md`.
- **OpenCode compatibility guide** (`docs/OPENCODE.md`): Skill/agent discovery, symlink instructions.
- **Contributing guide** (`CONTRIBUTING.md`): Skill development tutorial, quality checklist, PR process.
- **Subagent lifecycle rules**: Background launch, wait-for-all, 5-minute timeout, partial result handling.
- **Schema template updates**: Added WebApplication, SearchAction, ConferenceEvent, LoyaltyProgram templates.
- **Interactive setup wizard** (`scripts/interactive_setup.py`): Guided first-run configuration.
- **Example outputs** in `examples/` directory.
- **`requirements-optional.txt`**: Separate file for Playwright dependency.
- **`package.json`**: npm skill package metadata for distribution.
- **Enhanced `SECURITY.md`**: CVE tracking table, scope definition, detailed reporting process.

### Changed
- **Agent Bash scope reduced**: Removed Bash from seo-schema, seo-content, seo-sitemap, seo-technical agents. Replaced with WebFetch. Only seo-performance and seo-visual retain Bash.
- **seo-visual agent**: WebFetch primary, Playwright optional (screenshots only). ~200MB Chromium no longer required.
- **Playwright moved to optional**: Commented out in `requirements.txt`, available via `requirements-optional.txt`.
- **Skill count**: 23 → 32 sub-skills across 9 categories.
- **Content category expanded**: 9 → 10 skills (blog pipeline added).
- **Monitoring category expanded**: 3 → 6 skills (rank tracking, competitive tracking, CWV analytics).

---

## [1.2.0] - 2026-02-19

### Security
- **SSRF prevention**: Added private IP blocking to `fetch_page.py` and `analyze_visual.py`
- **Path traversal prevention**: Added output path sanitization to `capture_screenshot.py` and file validation to `parse_html.py`
- **Install hardening**: Removed `--break-system-packages`, switched to venv-based pip install
- **requirements.txt**: Now persisted to skill directory for user retry

### Fixed
- **YAML frontmatter parsing**: Removed HTML comments before `---` delimiter in 8 files (skills: seo-content, seo-images, seo-programmatic, seo-schema, seo-technical; agents: seo-content, seo-performance, seo-technical)
- **Windows installer**: Added `python -m pip`, `py -3` launcher fallback, requirements.txt persistence, non-fatal subagent copy, better error diagnostics
- **requirements.txt missing after install**: Now copied to skill directory so users can retry (#1)

### Changed
- Python dependencies now installed in a local venv with `--user` fallback (#2)
- Playwright marked as explicitly optional in install output
- Windows installer uses `Resolve-Python` helper for robust Python detection (#5)

---

## [1.1.0] - 2026-02-07

### Security (CRITICAL)
- **urllib3 ≥2.6.3**: Fixes CVE-2026-21441 (CVSS 8.9) - decompression bypass vulnerability
- **lxml ≥6.0.2**: Updated from 5.3.2 for additional libxml2 security patches
- **Pillow ≥12.1.0**: Fixes CVE-2025-48379
- **playwright ≥1.55.1**: Fixes CVE-2025-59288 (macOS)
- **requests ≥2.32.4**: Fixes CVE-2024-47081, CVE-2024-35195

### Added
- **GEO (Generative Engine Optimization) major enhancement**:
  - Brand mention analysis (3× more important than backlinks for AI visibility)
  - AI crawler detection (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, etc.)
  - llms.txt standard detection and recommendations
  - RSL 1.0 (Really Simple Licensing) detection
  - Passage-level citability scoring (optimal 134-167 words)
  - Platform-specific optimization (Google AI Overviews vs ChatGPT vs Perplexity)
  - Server-side rendering checks for AI crawler accessibility
- **LCP Subparts analysis**: TTFB, resource load delay, resource load time, render delay
- **Soft Navigations API detection** for SPA CWV measurement limitations
- **Schema.org v29.4 additions**: ConferenceEvent, PerformingArtsEvent, LoyaltyProgram
- **E-commerce schema updates**: returnPolicyCountry now required, organization-level policies

### Changed
- **E-E-A-T framework**: Updated for December 2025 core update - now applies to ALL competitive queries, not just YMYL
- **SKILL.md description**: Expanded to leverage new 1024-character limit
- **Schema deprecations expanded**: Added ClaimReview, VehicleListing (June 2025)
- **WebApplication schema**: Added as correct type for browser-based SaaS (vs SoftwareApplication)

### Fixed
- Schema-types.md now correctly distinguishes SoftwareApplication (apps) vs WebApplication (SaaS)

---

## [1.0.0] - 2026-02-07

### Added
- Initial release of 30x SEO
- 9 specialized skills: audit, page, sitemap, schema, images, technical, content, geo, plan
- 6 subagents for parallel analysis: seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance, seo-visual
- Industry templates: SaaS, local service, e-commerce, publisher, agency, generic
- Schema library with deprecation tracking:
  - HowTo schema marked deprecated (September 2023)
  - FAQ schema restricted to government/healthcare sites only (August 2023)
  - SpecialAnnouncement schema marked deprecated (July 31, 2025)
- AI Overviews / GEO optimization skill (seo-geo) - new for 2026
- Core Web Vitals analysis using current metrics:
  - LCP (Largest Contentful Paint): <2.5s
  - INP (Interaction to Next Paint): <200ms - replaced FID on March 12, 2024
  - CLS (Cumulative Layout Shift): <0.1
- E-E-A-T framework updated to September 2025 Quality Rater Guidelines
- Quality gates for thin content and doorway page prevention:
  - Warning at 30+ location pages
  - Hard stop at 50+ location pages
- Pre-commit and post-edit automation hooks
- One-command install and uninstall scripts (Unix and Windows)
- Bounded Python dependency pinning with CVE-aware minimums (lxml >= 5.3.2)

### Architecture
- Follows Anthropic's official Claude Code skill specification (February 2026)
- Standard directory layout: `scripts/`, `references/`, `assets/`
- Valid hook matchers (tool name only, no argument patterns)
- Correct subagent frontmatter fields (name, description, tools)
- CLI command is `claude` (not `claude-code`)
