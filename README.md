```
██████╗  ██████╗ ██╗  ██╗    ███████╗███████╗ ██████╗
╚════██╗██╔═══██╗╚██╗██╔╝    ██╔════╝██╔════╝██╔═══██╗
 █████╔╝██║   ██║ ╚███╔╝     ███████╗█████╗  ██║   ██║
 ╚═══██╗██║   ██║ ██╔██╗     ╚════██║██╔══╝  ██║   ██║
██████╔╝╚██████╔╝██╔╝ ██╗    ███████║███████╗╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚══════╝ ╚═════╝
```

> 24 production-ready SEO skills + Squirrelscan CLI for Claude Code, organized in 9 categories. Full-stack SEO automation: audits, technical SEO, links, content, planning, programmatic SEO, monitoring, local SEO, and keyword research.

## Why 30x SEO?

- **Complete Coverage**: 9 categories, 24 skills, full SEO workflow
- **AI-Native**: Built for Claude Code, not retrofitted from legacy tools
- **2026 Ready**: AI Overviews, GEO optimization, LLM citation tracking
- **No MCP Dependencies**: Direct API calls, zero middleware issues

## Quick Start

```bash
npx skills add norahe0304-art/30x-seo
```

That's it. One command installs all 24 skills.

**Optional: Configure DataForSEO** (for keywords/backlinks/SERP/AI visibility)

```bash
echo -n "email:password" | base64 > ~/.config/dataforseo/auth
chmod 600 ~/.config/dataforseo/auth
```

---

## Skills Overview (9 Categories, 24 Skills + 1 Orchestrator)

### Main Orchestrator

| Skill | What it does |
|-------|--------------|
| `seo` | Master orchestrator: routes commands to 24 sub-skills, spawns 6 parallel subagents, auto-detects industry type |

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

### 4. Content (6 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-content-audit` | E-E-A-T scoring + AI citability analysis |
| `30x-seo-images` | Alt text, file sizes, formats (WebP/AVIF), lazy loading, CLS |
| `30x-seo-content-decay` | Detect declining content, recommend refresh priorities |
| `30x-seo-cannibalization` | Find keyword conflicts between pages |
| `30x-seo-content-brief` | Analyze SERP top 10, generate content briefs |
| `30x-seo-content-writer` | SEO + AI optimized writing guidelines |

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

### 7. Monitoring (3 skills)

| Skill | What it does |
|-------|--------------|
| `30x-seo-monitor` | Monitor your own site: rankings, clicks, CTR, position changes *(Google Search Console)* |
| `30x-seo-serp` | Track any site's SERP rankings, features, historical data *(DataForSEO)* |
| `30x-seo-ai-visibility` | Track mentions in ChatGPT, Claude, Perplexity, Gemini, AI Overview *(DataForSEO)* |

### 8. Local SEO (1 skill)

| Skill | What it does |
|-------|--------------|
| `30x-seo-local` | GBP audit, NAP consistency, review strategy, local schema, Gemini Ask Maps optimization |

### 9. Data (1 skill)

| Skill | What it does |
|-------|--------------|
| `30x-seo-keywords` | Ideas, volume, difficulty, intent, trends *(DataForSEO)* |

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
/seo backlinks profile example.com        # DataForSEO

# Content
/seo content-audit https://example.com/page
/seo content-brief "target keyword"

# Planning
/seo plan saas
/seo architecture https://example.com

# Programmatic
/seo programmatic plan
/seo competitor-pages generate

# Local SEO
/seo local "Business Name" https://example.com

# Monitoring
/seo monitor overview                     # GSC - your site
/seo monitor keywords                     # GSC - your rankings
/seo serp check "keyword"                 # DataForSEO - any site
/seo ai-visibility domain example.com     # DataForSEO

# Data
/seo keywords research "seed keyword"     # DataForSEO
```

---

## Dependencies

| Category | Skills | Dependency |
|----------|--------|------------|
| Audit | 1 | WebFetch |
| Technical SEO | 5 | WebFetch |
| Links | 3 | WebFetch + DataForSEO (backlinks) |
| Content | 6 | WebFetch |
| Planning | 2 | WebFetch |
| Programmatic SEO | 2 | WebFetch |
| Local SEO | 1 | WebFetch |
| Monitoring | 3 | GSC + DataForSEO |
| Data | 1 | DataForSEO |

**19 skills work without any API. 4 skills require DataForSEO. 1 skill requires Google Search Console.**

---

## DataForSEO Setup

1. Sign up at [app.dataforseo.com](https://app.dataforseo.com)
2. Get credentials: Settings → API Access
3. Create auth file:

```bash
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

## License

MIT
