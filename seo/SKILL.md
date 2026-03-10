---
name: seo
description: >
  Master SEO orchestrator with 32 specialized sub-skills across 9 categories.
  Comprehensive SEO analysis for any website or business type. Performs full site
  audits, single-page deep analysis, technical SEO checks (crawlability, indexability,
  Core Web Vitals with INP), schema markup, content quality (E-E-A-T framework),
  image optimization, sitemap analysis, site architecture planning, AI search
  optimization (GEO for ChatGPT, Perplexity, AI Overviews), backlink analysis,
  keyword research, SERP tracking, AI visibility monitoring, fake freshness detection,
  mobile content parity checks, and Google Discover optimization.
  Industry detection for SaaS, e-commerce, local business, publishers, agencies.
  Triggers on: "SEO", "audit", "schema", "Core Web Vitals", "sitemap", "E-E-A-T",
  "AI Overviews", "GEO", "technical SEO", "content quality", "page speed",
  "structured data", "site architecture", "metadata", "AI SEO", "backlinks",
  "link building", "keywords", "keyword research", "SERP", "AI visibility",
  "fake freshness", "mobile parity", "Discover", "rank tracking",
  "competitive tracking", "CWV analytics", "LCP subparts", "CrUX",
  "semantic search", "entity SEO", "Knowledge Graph", "content localization",
  "blog pipeline", "write blog", "generate article", "auto blog".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# SEO — Master Orchestrator (23 Sub-Skills)

[PROTOCOL]: Update this header on changes

Comprehensive SEO analysis across all industries (SaaS, local services,
e-commerce, publishers, agencies). Orchestrates **32 specialized sub-skills**
organized in 9 categories, plus 6 parallel subagents for audits.

---

## Quick Reference

### 1. Audit
| Command | What it does |
|---------|-------------|
| `/seo page <url>` | Deep single-page analysis: title, meta, headings, links, images, Schema, E-E-A-T |
| `squirrelscan audit <url>` | Full-site 230+ rules audit via CLI (`npm i -g squirrelscan`) |

### 2. Technical SEO
| Command | What it does |
|---------|-------------|
| `/seo technical <url>` | 8-category audit: crawl, index, security, URLs, mobile, CWV, structured data, JS |
| `/seo sitemap <url>` | Validate XML sitemaps, detect issues, generate new ones |
| `/seo hreflang <url>` | Multi-language SEO: self-refs, return tags, x-default, ISO codes |
| `/seo schema <url>` | Detect, validate, generate JSON-LD structured data |
| `/seo geo-technical <url>` | AI crawler management: GPTBot, ClaudeBot, llms.txt, SSR check |

### 3. Links
| Command | What it does |
|---------|-------------|
| `/seo internal-links <url>` | Orphan pages, click depth, anchor text, link equity |
| `/seo backlinks profile <domain>` | Backlink profile analysis *(DataForSEO)* |
| `/seo backlinks gap <domain> <competitor>` | Find link gap opportunities *(DataForSEO)* |
| `/seo redirects <url>` | Chains, loops, 301/302 mix, protocol issues, trailing slashes |

### 4. Content
| Command | What it does |
|---------|-------------|
| `/seo content-audit <url>` | E-E-A-T scoring + AI citability analysis |
| `/seo images <url>` | Alt text, file sizes, formats (WebP/AVIF), lazy loading, CLS |
| `/seo content-decay <url>` | Detect declining content, recommend refresh priorities |
| `/seo cannibalization <domain>` | Find keyword conflicts between pages |
| `/seo content-brief <keyword>` | Analyze SERP top 10, generate content briefs |
| `/seo content-writer` | SEO + AI optimized writing guidelines |
| `/seo fake-freshness <url>` | Detect pages with updated dates but unchanged content |
| `/seo mobile-parity <url>` | Compare mobile vs desktop content for indexing parity |
| `/seo discover <url>` | Google Discover optimization: clickbait, depth, images |
| `/seo blog-pipeline <keyword>` | Full blog production: research → outline → draft → optimize |

### 5. Planning
| Command | What it does |
|---------|-------------|
| `/seo plan <business-type>` | Competitor analysis, keyword strategy, content calendar, 4-phase roadmap |
| `/seo architecture <url>` | URL structure, navigation design, internal linking strategy |

### 6. Programmatic SEO
| Command | What it does |
|---------|-------------|
| `/seo programmatic plan` | Scale content: data sources, templates, quality gates, index control |
| `/seo competitor-pages generate` | X vs Y comparisons, alternatives pages, feature matrices |

### 7. Monitoring
| Command | What it does |
|---------|-------------|
| `/seo monitor overview` | Monitor your site: rankings, clicks, CTR, position changes *(GSC)* |
| `/seo serp check <keyword>` | Live SERP check for any keyword *(DataForSEO)* |
| `/seo ai-visibility domain <domain>` | Track mentions in ChatGPT, Claude, Perplexity, AI Overview *(DataForSEO)* |
| `/seo rank-tracking snapshot <domain>` | Current rankings + position history + alerts *(DataForSEO)* |
| `/seo competitive-tracking overview <domain> <competitor>` | Side-by-side competitor monitoring *(DataForSEO)* |
| `/seo cwv-analytics overview <url>` | CrUX field data + LCP subparts + INP diagnostics *(Google API)* |

### 8. Data
| Command | What it does |
|---------|-------------|
| `/seo keywords research <seed>` | Ideas, volume, difficulty, intent, trends *(DataForSEO)* |
| `/seo keywords site <domain>` | Keywords a site ranks for *(DataForSEO)* |
| `/seo keywords gap <domain> <competitor>` | Find keyword opportunities *(DataForSEO)* |

### 9. Advanced
| Command | What it does |
|---------|-------------|
| `/seo semantic-search <url>` | Entity extraction, topical authority, Knowledge Graph optimization |
| `/seo content-localization <source-url> <localized-url>` | Translation quality, cultural adaptation, locale keywords |

---

## Command → Skill Routing

| Command | Loads Skill |
|---------|-------------|
| `page` | 30x-seo-page |
| `technical` | 30x-seo-technical |
| `sitemap` | 30x-seo-sitemap |
| `hreflang` | 30x-seo-hreflang |
| `schema` | 30x-seo-schema |
| `geo-technical` | 30x-seo-geo-technical |
| `internal-links` | 30x-seo-internal-links |
| `backlinks` | 30x-seo-backlinks |
| `redirects` | 30x-seo-redirects |
| `content-audit` | 30x-seo-content-audit |
| `images` | 30x-seo-images |
| `content-decay` | 30x-seo-content-decay |
| `cannibalization` | 30x-seo-cannibalization |
| `content-brief` | 30x-seo-content-brief |
| `content-writer` | 30x-seo-content-writer |
| `fake-freshness` | 30x-seo-fake-freshness |
| `mobile-parity` | 30x-seo-mobile-parity |
| `discover` | 30x-seo-discover |
| `rank-tracking` | 30x-seo-rank-tracking |
| `competitive-tracking` | 30x-seo-competitive-tracking |
| `cwv-analytics` | 30x-seo-cwv-analytics |
| `semantic-search` | 30x-seo-semantic-search |
| `content-localization` | 30x-seo-content-localization |
| `blog-pipeline` | 30x-seo-blog-pipeline |
| `plan` | 30x-seo-plan |
| `architecture` | 30x-seo-architecture |
| `programmatic` | 30x-seo-programmatic |
| `competitor-pages` | 30x-seo-competitor-pages |
| `monitor` | 30x-seo-monitor |
| `serp` | 30x-seo-serp |
| `ai-visibility` | 30x-seo-ai-visibility |
| `keywords` | 30x-seo-keywords |

---

## Orchestration Logic

When user invokes `/seo audit`, delegate to subagents in parallel:
1. Detect business type (SaaS, local, ecommerce, publisher, agency, other)
2. Spawn subagents: technical, content, schema, sitemap, performance, visual
3. Collect results and generate unified report with SEO Health Score (0-100)
4. Create prioritized action plan (Critical → High → Medium → Low)

### Subagent Lifecycle Rules

- **Launch**: Spawn all 6 subagents using the Agent tool with `run_in_background: true`
- **Wait**: Do NOT generate the final report until all subagents have returned results. You will be notified when each completes.
- **Timeout**: If a subagent has not returned after 5 minutes, proceed without it and note the gap in the report.
- **Context management**: For large pages, subagents should focus on their specific domain only. Do not ask subagents to analyze areas outside their specialty.
- **Partial results**: If any subagent fails, include available results and flag missing sections as "Analysis unavailable — [agent] did not complete."

---

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce**: /products, /collections, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
- **Agency**: /case-studies, /portfolio, /industries, "our work", client logos

---

## Quality Gates

Hard rules:
- WARNING at 30+ location pages (enforce 60%+ unique content)
- HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID

---

## Scoring Methodology

### SEO Health Score (0-100)

| Category | Weight |
|----------|--------|
| Technical SEO | 25% |
| Content Quality | 25% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| Images | 5% |
| AI Search Readiness | 5% |

### Priority Levels
- **Critical**: Blocks indexing or causes penalties (immediate fix)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## Sub-Skills (32 Total, 9 Categories)

### 1. Audit (1 skill + CLI)
| Skill | What it does |
|-------|-------------|
| **30x-seo-page** | Deep single-page analysis |
| **squirrelscan** *(CLI)* | Full-site 230+ rules audit |

### 2. Technical SEO (5 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-technical** | 8-category technical audit |
| **30x-seo-sitemap** | Sitemap validation and generation |
| **30x-seo-hreflang** | International SEO / hreflang |
| **30x-seo-schema** | Schema.org JSON-LD |
| **30x-seo-geo-technical** | AI crawler management |

### 3. Links (3 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-internal-links** | Internal link analysis |
| **30x-seo-backlinks** | Backlink profile *(DataForSEO)* |
| **30x-seo-redirects** | Redirect chain analysis |

### 4. Content (10 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-content-audit** | E-E-A-T + AI citability |
| **30x-seo-images** | Image optimization |
| **30x-seo-content-decay** | Content freshness analysis |
| **30x-seo-cannibalization** | Keyword conflict detection |
| **30x-seo-content-brief** | SERP-based content briefs |
| **30x-seo-content-writer** | SEO writing guidelines |
| **30x-seo-fake-freshness** | Detect fake date updates |
| **30x-seo-mobile-parity** | Mobile vs desktop content parity |
| **30x-seo-discover** | Google Discover optimization |
| **30x-seo-blog-pipeline** | End-to-end SEO blog production |

### 5. Planning (2 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-plan** | Strategic SEO planning |
| **30x-seo-architecture** | Site structure planning |

### 6. Programmatic SEO (2 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-programmatic** | Scale content with templates |
| **30x-seo-competitor-pages** | X vs Y comparison pages |

### 7. Monitoring (6 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-monitor** | Your site via GSC |
| **30x-seo-serp** | Any site via DataForSEO |
| **30x-seo-ai-visibility** | AI search visibility |
| **30x-seo-rank-tracking** | Historical rank tracking + alerts |
| **30x-seo-competitive-tracking** | Competitor SERP monitoring |
| **30x-seo-cwv-analytics** | CrUX field data + CWV deep dive |

### 8. Data (1 skill)
| Skill | What it does |
|-------|-------------|
| **30x-seo-keywords** | Keyword research *(DataForSEO)* |

### 9. Advanced (2 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-semantic-search** | Entity extraction + Knowledge Graph |
| **30x-seo-content-localization** | Multi-language content quality |

---

## Dependencies

| Category | Skills | Dependency |
|----------|--------|------------|
| Audit | 1 | WebFetch |
| Technical SEO | 5 | WebFetch |
| Links | 3 | WebFetch + DataForSEO (backlinks) |
| Content | 7 | WebFetch |
| Planning | 2 | WebFetch |
| Programmatic SEO | 2 | WebFetch |
| Monitoring | 6 | GSC + DataForSEO + Google API |
| Data | 1 | DataForSEO |

**23 skills work without any API. 6 skills require DataForSEO. 1 skill requires GSC. 1 skill requires Google API key (CrUX/PSI).**

---

## Subagents

For parallel analysis during audits:
- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-performance` — Core Web Vitals measurement
- `seo-visual` — Screenshots, mobile testing, above-fold
