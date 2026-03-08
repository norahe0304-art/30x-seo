# 30x SEO

> 21 production-ready SEO skills for Claude Code. Full-stack SEO automation: technical audits, content optimization, keyword research, backlink analysis, and AI visibility monitoring.

## Why 30x SEO?

- **Complete Coverage**: Technical SEO → Content → Keywords → Backlinks → AI Visibility
- **AI-Native**: Built for Claude Code, not retrofitted from legacy tools
- **2026 Ready**: AI Overviews, GEO optimization, LLM citation tracking
- **No MCP Dependencies**: Direct API calls, zero middleware issues

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/30x-seo.git ~/.openclaw/skills/30x-seo

# Configure DataForSEO (for keywords/backlinks/SERP/AI visibility)
mkdir -p ~/.config/dataforseo
echo "YOUR_BASE64_CREDENTIALS" > ~/.config/dataforseo/auth
chmod 600 ~/.config/dataforseo/auth
```

**Generate Base64 credentials:**
```bash
echo -n "email@example.com:api-password" | base64
```

## Skills Overview

### Technical SEO (8 skills)

| Skill | What it does |
|-------|--------------|
| `seo-technical` | 8-category audit: crawlability, indexability, security, URLs, mobile, Core Web Vitals, structured data, JS rendering |
| `seo-sitemap` | Validate XML sitemaps, detect issues, generate new ones |
| `seo-hreflang` | Multi-language/region SEO: self-refs, return tags, x-default |
| `seo-schema` | Detect, validate, generate JSON-LD structured data |
| `seo-images` | Alt text, formats, sizing, lazy loading, CDN usage |
| `seo-redirects` | Chains, loops, soft 404s, external leaks |
| `seo-internal-links` | Orphan pages, click depth, anchor text, link equity |
| `seo-geo-technical` | AI crawler management: GPTBot, ClaudeBot, llms.txt |

### Content Optimization (8 skills)

| Skill | What it does |
|-------|--------------|
| `seo-content-audit` | E-E-A-T scoring + AI citability analysis |
| `seo-content-brief` | Generate briefs from keyword research |
| `seo-content-writer` | Writing guidelines for SEO + AI optimization |
| `seo-content-decay` | Detect declining content, recommend updates |
| `seo-cannibalization` | Find keyword conflicts between pages |
| `seo-page` | Deep single-page analysis |
| `seo-competitor-pages` | Compare against SERP top 10 |
| `seo-programmatic` | Scale content with quality gates |

### Keywords & SERP (3 skills) — *Requires DataForSEO*

| Skill | What it does |
|-------|--------------|
| `seo-keywords` | Ideas, volume, difficulty, intent, trends |
| `seo-serp` | Live SERP, rankings, historical data, features |
| `seo-backlinks` | Profile, anchors, toxic links, gap analysis |

### AI Visibility (2 skills) — *Requires DataForSEO*

| Skill | What it does |
|-------|--------------|
| `seo-ai-visibility` | Track brand mentions in ChatGPT, Claude, Perplexity, Gemini, Google AI Overview |
| `seo-plan` | Generate comprehensive SEO strategy |

## Commands

```bash
# Technical
/seo technical https://example.com
/seo schema https://example.com
/seo sitemap analyze https://example.com/sitemap.xml

# Content
/seo content-audit https://example.com/page
/seo content-brief "target keyword"

# Keywords & SERP (DataForSEO required)
/seo keywords research "seed keyword"
/seo serp check "keyword"
/seo backlinks profile example.com

# AI Visibility (DataForSEO required)
/seo ai-visibility domain example.com
/seo ai-visibility keyword "best crm software"
```

## Architecture

```
30x-seo/
├── skills/           # 21 SEO skills
│   └── 30x-seo-*/    # Individual skill directories
├── agents/           # 6 subagents for parallel execution
├── docs/             # Architecture, commands, MCP integration
├── schema/           # JSON-LD templates
└── seo/              # Main skill + reference materials
```

## Dependencies

| Skill Category | Count | Dependency |
|----------------|-------|------------|
| Technical SEO | 8 | WebFetch (built-in) |
| Content | 8 | WebFetch (built-in) |
| Keywords/SERP/Backlinks | 3 | DataForSEO API |
| AI Visibility | 2 | DataForSEO API |

**16 skills work without any API configuration.**

## DataForSEO Setup

1. Sign up at [app.dataforseo.com](https://app.dataforseo.com)
2. Get credentials from Settings → API Access
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

## What's Included

- **9,300+ lines** of SEO guidance
- **2025-2026 updates**: INP metrics, AI Overview optimization, E-E-A-T guidelines
- **AI visibility monitoring**: Track citations across LLMs
- **GEO optimization**: Generative Engine Optimization for AI search
- **Quality gates**: Prevent thin content, doorway pages

## License

MIT
