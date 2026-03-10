```
██████╗  ██████╗ ██╗  ██╗    ███████╗███████╗ ██████╗
╚════██╗██╔═══██╗╚██╗██╔╝    ██╔════╝██╔════╝██╔═══██╗
 █████╔╝██║   ██║ ╚███╔╝     ███████╗█████╗  ██║   ██║
 ╚═══██╗██║   ██║ ██╔██╗     ╚════██║██╔══╝  ██║   ██║
██████╔╝╚██████╔╝██╔╝ ██╗    ███████║███████╗╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚══════╝ ╚═════╝
```

> 32 production-ready SEO skills + Squirrelscan CLI for Claude Code, organized in 9 categories. Full-stack SEO automation: audits, technical SEO, links, content, planning, programmatic SEO, monitoring, keyword research, and advanced entity/localization analysis.

## Why 30x SEO?

- **Complete Coverage**: 9 categories, 32 skills, full SEO workflow
- **AI-Native**: Built for Claude Code, not retrofitted from legacy tools
- **2026 Ready**: AI Overviews, GEO optimization, LLM citation tracking, INP metrics
- **No MCP Dependencies**: Direct API calls, zero middleware issues
- **Tested**: 257+ automated tests, CI/CD pipeline, health checks

## Quick Start

```bash
npx skills add norahe0304-art/30x-seo
```

That's it. One command installs all 32 skills.

**First-time setup (interactive):**

```bash
python3 scripts/interactive_setup.py
```

Guides you through DataForSEO credentials, Google API key, and optional Playwright setup.

**Or configure manually:**

```bash
# DataForSEO (for keywords/backlinks/SERP/AI visibility/rank tracking)
mkdir -p ~/.config/dataforseo
echo -n "email:password" | base64 > ~/.config/dataforseo/auth
chmod 600 ~/.config/dataforseo/auth

# Google API key (for CrUX/PageSpeed Insights)
mkdir -p ~/.config/google
echo "YOUR_API_KEY" > ~/.config/google/api_key
chmod 600 ~/.config/google/api_key
```

**Verify installation:**

```bash
python3 scripts/health_check.py
```

---

## Skills Overview (9 Categories, 32 Skills + 1 Orchestrator)

### Main Orchestrator

| Skill | What it does |
|-------|--------------|
| `seo` | Master orchestrator: routes commands to 32 sub-skills, spawns 6 parallel subagents, auto-detects industry type |

### 1. Audit (1 skill + CLI)

| Skill | What it does |
|-------|--------------|
| `30x-seo-page` | Deep single-page analysis: title, meta, headings, links, images, Schema, E-E-A-T |
| `squirrelscan` *(CLI)* | Full-site audit: 230+ rules, 21 categories, health score 0-100. Install: `npm i -g squirrelscan` |

### 2. Technical SEO (5 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-technical` | 8-category audit: crawlability, indexability, security, URLs, mobile, CWV, structured data, JS |
| `30x-seo-sitemap` | Validate XML sitemaps, detect issues, generate new ones |
| `30x-seo-hreflang` | Multi-language SEO: self-refs, return tags, x-default, ISO codes |
| `30x-seo-schema` | Detect, validate, generate JSON-LD structured data |
| `30x-seo-geo-technical` | AI crawler management: GPTBot, ClaudeBot, llms.txt, SSR check |

### 3. Links (3 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-internal-links` | Orphan pages, click depth, anchor text, link equity distribution |
| `30x-seo-backlinks` | Profile, anchors, toxic links, gap analysis *(DataForSEO)* |
| `30x-seo-redirects` | Chains, loops, 301/302 mix, protocol issues, trailing slashes |

### 4. Content (10 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-content-audit` | E-E-A-T scoring + AI citability analysis |
| `30x-seo-images` | Alt text, file sizes, formats (WebP/AVIF), lazy loading, CLS |
| `30x-seo-content-decay` | Detect declining content, recommend refresh priorities |
| `30x-seo-cannibalization` | Find keyword conflicts between pages |
| `30x-seo-content-brief` | Analyze SERP top 10, generate content briefs |
| `30x-seo-content-writer` | SEO + AI optimized writing guidelines |
| `30x-seo-fake-freshness` | Detect pages with updated dates but unchanged content |
| `30x-seo-mobile-parity` | Compare mobile vs desktop content for indexing parity |
| `30x-seo-discover` | Google Discover optimization: clickbait, depth, images |
| `30x-seo-blog-pipeline` | End-to-end SEO blog production: research → outline → draft → optimize |

### 5. Planning (2 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-plan` | Competitor analysis, keyword strategy, content calendar, 4-phase roadmap |
| `30x-seo-architecture` | URL structure, navigation design, internal linking strategy |

### 6. Programmatic SEO (2 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-programmatic` | Scale content: data sources, templates, quality gates, index control |
| `30x-seo-competitor-pages` | X vs Y comparisons, alternatives pages, feature matrices |

### 7. Monitoring (6 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-monitor` | Monitor your own site: rankings, clicks, CTR, position changes *(GSC)* |
| `30x-seo-serp` | Track any site's SERP rankings, features, historical data *(DataForSEO)* |
| `30x-seo-ai-visibility` | Track mentions in ChatGPT, Claude, Perplexity, Gemini, AI Overview *(DataForSEO)* |
| `30x-seo-rank-tracking` | Historical rank tracking, position change alerts, trending keywords *(DataForSEO)* |
| `30x-seo-competitive-tracking` | Competitor SERP monitoring, threat detection, new content alerts *(DataForSEO)* |
| `30x-seo-cwv-analytics` | CrUX field data, LCP subparts, INP diagnostics *(Google API)* |

### 8. Data (1 skill)

| Skill | What it does |
|-------|--------------|
| `30x-seo-keywords` | Ideas, volume, difficulty, intent, trends *(DataForSEO)* |

### 9. Advanced (2 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-semantic-search` | Entity extraction, topical authority, Knowledge Graph optimization |
| `30x-seo-content-localization` | Translation quality, cultural adaptation, locale-specific keywords |

---

## Commands

```bash
# Audit
/seo page https://example.com/page
squirrelscan audit https://example.com --format llm

# Technical
/seo technical https://example.com
/seo schema https://example.com
/seo sitemap https://example.com/sitemap.xml

# Links
/seo internal-links https://example.com
/seo redirects https://example.com
/seo backlinks profile example.com              # DataForSEO

# Content
/seo content-audit https://example.com/page
/seo content-brief "target keyword"
/seo fake-freshness https://example.com/page
/seo mobile-parity https://example.com/page
/seo discover https://example.com/page
/seo blog-pipeline "target keyword"

# Planning
/seo plan saas
/seo architecture https://example.com

# Programmatic
/seo programmatic plan
/seo competitor-pages generate

# Monitoring
/seo monitor overview                           # GSC - your site
/seo serp check "keyword"                       # DataForSEO
/seo ai-visibility domain example.com           # DataForSEO
/seo rank-tracking snapshot example.com          # DataForSEO
/seo competitive-tracking overview me.com rival.com  # DataForSEO
/seo cwv-analytics overview https://example.com  # Google API

# Data
/seo keywords research "seed keyword"           # DataForSEO

# Advanced
/seo semantic-search https://example.com/page
/seo content-localization https://example.com/en/page https://example.com/de/page
```

---

## Dependencies

| Category | Skills | Dependency |
|----------|--------|------------|
| Audit | 1 | WebFetch |
| Technical SEO | 5 | WebFetch |
| Links | 3 | WebFetch + DataForSEO (backlinks) |
| Content | 10 | WebFetch |
| Planning | 2 | WebFetch |
| Programmatic SEO | 2 | WebFetch |
| Monitoring | 6 | GSC + DataForSEO + Google API |
| Data | 1 | DataForSEO |
| Advanced | 2 | WebFetch |

**23 skills work without any API. 6 skills require DataForSEO. 1 skill requires GSC. 1 skill requires Google API key.**

---

## DataForSEO Setup

1. Sign up at [app.dataforseo.com](https://app.dataforseo.com)
2. Get credentials: Settings > API Access
3. Create auth file:

```bash
mkdir -p ~/.config/dataforseo
echo -n "your-email:your-password" | base64 > ~/.config/dataforseo/auth
chmod 600 ~/.config/dataforseo/auth
```

4. Verify:

```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "test", "limit": 1}]' | jq '.status_code'
# Returns 20000 = success
```

---

## Development

```bash
# Clone and set up dev environment
git clone https://github.com/norahe0304-art/30x-seo.git
cd 30x-seo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linter
ruff check scripts/ tests/

# Health check
python3 scripts/health_check.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for skill development guide.

---

## Docker (optional sandboxing)

```bash
# Lightweight (no Playwright)
docker build -t 30x-seo-scripts .
docker run --rm 30x-seo-scripts scripts/fetch_page.py https://example.com

# With screenshots
docker build -f Dockerfile.playwright -t 30x-seo-scripts-pw .
docker run --rm -v "$(pwd)/screenshots:/app/screenshots" \
  30x-seo-scripts-pw scripts/capture_screenshot.py https://example.com --all
```

See [docs/DOCKER.md](docs/DOCKER.md) for details.

---

## Documentation

| Doc | Description |
|-----|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, orchestration flow, directory structure |
| [COMMANDS.md](docs/COMMANDS.md) | Full command reference |
| [INSTALLATION.md](docs/INSTALLATION.md) | Detailed setup guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Skill development guide, quality checklist |
| [DOCKER.md](docs/DOCKER.md) | Docker sandboxed execution |
| [OPENCODE.md](docs/OPENCODE.md) | OpenCode compatibility |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting, CVE tracking |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## License

MIT
