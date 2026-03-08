---
name: seo
description: >
  Master SEO orchestrator with 23 specialized sub-skills. Comprehensive SEO analysis
  for any website or business type. Performs full site audits (squirrelscan 230+ rules,
  parallel subagent delegation), single-page deep analysis, technical SEO checks
  (crawlability, indexability, Core Web Vitals with INP), schema markup, content quality
  (E-E-A-T framework), image optimization, sitemap analysis, site architecture planning,
  metadata fixes, AI search optimization (GEO for ChatGPT, Perplexity, AI Overviews),
  backlink analysis (link building, toxic links, competitor links), and keyword research
  (search volume, difficulty, keyword gap).
  Industry detection for SaaS, e-commerce, local business, publishers, agencies.
  Triggers on: "SEO", "audit", "schema", "Core Web Vitals", "sitemap", "E-E-A-T",
  "AI Overviews", "GEO", "technical SEO", "content quality", "page speed",
  "structured data", "site architecture", "metadata", "AI SEO", "backlinks",
  "link building", "keywords", "keyword research".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# SEO — Master SEO Orchestrator (21 Sub-Skills)

Comprehensive SEO analysis across all industries (SaaS, local services,
e-commerce, publishers, agencies). Orchestrates **21 specialized sub-skills**
and 6 subagents.

## Quick Reference

### Diagnosis & Audit
| Command | What it does |
|---------|-------------|
| `/seo audit <url>` | Squirrelscan 230+ rules comprehensive audit |
| `/seo audit-lite <url>` | Quick SEO diagnosis (no CLI required) |
| `/seo page <url>` | Deep single-page analysis |

### Technical SEO
| Command | What it does |
|---------|-------------|
| `/seo technical <url>` | Technical SEO audit (8 categories) |
| `/seo sitemap <url or generate>` | Analyze or generate XML sitemaps |
| `/seo hreflang [url]` | Hreflang/i18n SEO audit and generation |
| `/seo metadata <url>` | Fix title, OG tags, canonical, Twitter cards |
| `/seo schema <url>` | Detect, validate, and generate Schema.org markup |

### Content & Images
| Command | What it does |
|---------|-------------|
| `/seo content <url>` | E-E-A-T and content quality analysis |
| `/seo images <url>` | Image optimization analysis |
| `/seo content-strategy` | Plan what content to create |

### Planning & Architecture
| Command | What it does |
|---------|-------------|
| `/seo plan <business-type>` | Strategic SEO planning |
| `/seo architecture` | Site structure, URL patterns, internal linking |
| `/seo programmatic [url\|plan]` | Programmatic SEO analysis and planning |
| `/seo competitor-pages [url\|generate]` | X vs Y comparison page generation |

### AI Search Optimization
| Command | What it does |
|---------|-------------|
| `/seo geo <url>` | GEO optimization (traditional + AI search) |
| `/seo ai <url>` | AI-specific optimization (ChatGPT, Perplexity citations) |

### Link Building
| Command | What it does |
|---------|-------------|
| `/seo backlinks <domain>` | Full backlink profile analysis |
| `/seo backlinks gap <domain> <competitor>` | Find link gap opportunities |
| `/seo backlinks toxic <domain>` | Detect potentially toxic links |

### Keyword Research
| Command | What it does |
|---------|-------------|
| `/seo keywords <seed>` | Keyword research and ideas |
| `/seo keywords site <domain>` | Keywords a site ranks for |
| `/seo keywords gap <domain> <competitor>` | Find keyword opportunities |

### AI Monitoring
| Command | What it does |
|---------|-------------|
| `/seo ai-monitor brand <brand>` | Track brand presence in AI search |
| `/seo ai-monitor keywords <kw1, kw2>` | Monitor AI citations for keywords |
| `/seo ai-monitor competitors <brand> <comp>` | Compare AI visibility vs competitors |

### SERP Tracking
| Command | What it does |
|---------|-------------|
| `/seo serp rank <domain>` | Get all keywords domain ranks for |
| `/seo serp check <keyword>` | Live SERP check for keyword |
| `/seo serp history <keyword>` | Historical SERP changes |

## Orchestration Logic

When the user invokes `/seo audit`, delegate to subagents in parallel:
1. Detect business type (SaaS, local, ecommerce, publisher, agency, other)
2. Spawn subagents: seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance, seo-visual
3. Collect results and generate unified report with SEO Health Score (0-100)
4. Create prioritized action plan (Critical → High → Medium → Low)

For individual commands, load the relevant sub-skill directly:

| Command | Loads Skill |
|---------|-------------|
| `audit` | squirrelscan-audit |
| `audit-lite` | seo-audit-lite |
| `page` | seo-page |
| `technical` | seo-technical |
| `sitemap` | seo-sitemap |
| `hreflang` | seo-hreflang |
| `metadata` | fixing-metadata |
| `schema` | seo-schema |
| `content` | seo-content |
| `images` | seo-images |
| `content-strategy` | content-strategy |
| `plan` | seo-plan |
| `architecture` | site-architecture |
| `programmatic` | seo-programmatic |
| `competitor-pages` | seo-competitor-pages |
| `geo` | seo-geo |
| `ai` | ai-seo |
| `backlinks` | seo-backlinks |
| `keywords` | seo-keywords |
| `ai-monitor` | seo-ai-monitor |
| `serp` | seo-serp |

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce**: /products, /collections, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
- **Agency**: /case-studies, /portfolio, /industries, "our work", client logos

## Quality Gates

Read `references/quality-gates.md` for thin content thresholds per page type.
Hard rules:
- WARNING at 30+ location pages (enforce 60%+ unique content)
- HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID

## Reference Files

Load these on-demand as needed — do NOT load all at startup:
- `references/cwv-thresholds.md` — Current Core Web Vitals thresholds and measurement details
- `references/schema-types.md` — All supported schema types with deprecation status
- `references/eeat-framework.md` — E-E-A-T evaluation criteria (Sept 2025 QRG update)
- `references/quality-gates.md` — Content length minimums, uniqueness thresholds

## Scoring Methodology

### SEO Health Score (0-100)
Weighted aggregate of all categories:

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
- **Critical**: Blocks indexing or causes penalties (immediate fix required)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Sub-Skills (21 Total)

### Diagnosis & Audit (3)
1. **squirrelscan-audit** — Comprehensive 230+ rules audit via squirrelscan CLI
2. **seo-audit-lite** — Quick SEO diagnosis for fast insights
3. **seo-page** — Deep single-page analysis

### Technical SEO (5)
4. **seo-technical** — Technical SEO (8 categories: crawl, index, security, CWV)
5. **seo-sitemap** — Sitemap analysis and generation
6. **seo-hreflang** — International SEO / hreflang tags
7. **fixing-metadata** — HTML meta tags, OG, canonical, Twitter cards
8. **seo-schema** — Schema.org JSON-LD detection, validation, generation

### Content & Images (3)
9. **seo-content** — E-E-A-T and content quality analysis
10. **seo-images** — Image optimization (alt, format, lazy load)
11. **content-strategy** — Content planning and topic clusters

### Planning & Architecture (4)
12. **seo-plan** — Strategic SEO planning with templates
13. **site-architecture** — URL structure, page hierarchy, internal linking
14. **seo-programmatic** — Programmatic SEO at scale
15. **seo-competitor-pages** — X vs Y comparison page generation

### AI Search Optimization (2)
16. **seo-geo** — GEO optimization (traditional + AI search combined)
17. **ai-seo** — AI citation optimization (ChatGPT, Perplexity, Claude)

### Link Building (1)
18. **seo-backlinks** — Backlink profile analysis, link gap, toxic link detection (DataForSEO)

### Keyword Research (1)
19. **seo-keywords** — Keyword research, search volume, difficulty, ranking analysis (DataForSEO)

### AI Monitoring (1)
20. **seo-ai-monitor** — Brand visibility tracking in AI search (ChatGPT, Perplexity, AI Overviews)

### SERP Tracking (1)
21. **seo-serp** — SERP rankings, position monitoring, SERP feature analysis (DataForSEO)

## Subagents

For parallel analysis during audits:
- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-performance` — Core Web Vitals measurement
- `seo-visual` — Screenshots, mobile testing, above-fold

## Skill Paths

External skills are loaded from these paths:
- `claude-seo/skills/` — Core SEO skills (15) including seo-backlinks, seo-keywords, seo-ai-monitor, seo-serp
- `marketingskills/skills/` — ai-seo, seo-audit-lite, site-architecture
- `squirrelscan/audit-website/` — squirrelscan-audit
- `ui-skills/` — fixing-metadata
- Root openclaw/skills/ — content-strategy
