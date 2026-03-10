# Commands Reference

## Overview

All 30x SEO commands start with `/seo` followed by a subcommand. 32 skills across 9 categories.

## Quick Reference

| Command | Use Case | Dependency |
|---------|----------|------------|
| `/seo audit <url>` | Full website audit (6 parallel subagents) | WebFetch |
| `/seo page <url>` | Deep single-page analysis | WebFetch |
| `/seo technical <url>` | 8-category technical SEO audit | WebFetch |
| `/seo schema <url>` | Schema detection, validation, generation | WebFetch |
| `/seo sitemap <url>` | Sitemap validation or generation | WebFetch |
| `/seo hreflang <url>` | International SEO / hreflang audit | WebFetch |
| `/seo geo-technical <url>` | AI crawler management, llms.txt | WebFetch |
| `/seo internal-links <url>` | Orphan pages, click depth, anchor text | WebFetch |
| `/seo backlinks profile <domain>` | Backlink profile analysis | DataForSEO |
| `/seo backlinks gap <domain> <competitor>` | Link gap opportunities | DataForSEO |
| `/seo redirects <url>` | Redirect chains, loops, protocol issues | WebFetch |
| `/seo content-audit <url>` | E-E-A-T + AI citability scoring | WebFetch |
| `/seo images <url>` | Alt text, sizes, formats, lazy loading | WebFetch |
| `/seo content-decay <url>` | Detect declining content | WebFetch |
| `/seo cannibalization <domain>` | Keyword conflict detection | WebFetch |
| `/seo content-brief <keyword>` | SERP-based content briefs | WebFetch |
| `/seo content-writer` | SEO writing guidelines | — |
| `/seo fake-freshness <url>` | Detect fake date updates | WebFetch |
| `/seo mobile-parity <url>` | Mobile vs desktop content parity | WebFetch |
| `/seo discover <url>` | Google Discover optimization | WebFetch |
| `/seo plan <type>` | Strategic SEO planning | WebFetch |
| `/seo architecture <url>` | Site structure planning | WebFetch |
| `/seo programmatic plan` | Scale content with templates | WebFetch |
| `/seo competitor-pages generate` | X vs Y comparison pages | WebFetch |
| `/seo monitor overview` | Your site via GSC | GSC |
| `/seo serp check <keyword>` | Live SERP check | DataForSEO |
| `/seo ai-visibility domain <domain>` | AI platform mentions | DataForSEO |
| `/seo rank-tracking snapshot <domain>` | Current rankings + alerts | DataForSEO |
| `/seo competitive-tracking overview <domain> <competitor>` | Competitor monitoring | DataForSEO |
| `/seo cwv-analytics overview <url>` | CrUX field data + LCP subparts | Google API |
| `/seo keywords research <seed>` | Keyword ideas + volume | DataForSEO |
| `/seo semantic-search <url>` | Entity extraction + Knowledge Graph | WebFetch |
| `/seo content-localization <source> <localized>` | Translation quality check | WebFetch |
| `/seo blog-pipeline <keyword>` | Full blog production pipeline | WebFetch |

---

## Command Details

### Audit

#### `/seo audit <url>`

Full website SEO audit with parallel analysis.

```
/seo audit https://example.com
```

1. Detects business type (SaaS, local, ecommerce, publisher, agency)
2. Spawns 6 specialist subagents in parallel
3. Generates SEO Health Score (0-100)
4. Creates prioritized action plan (Critical > High > Medium > Low)

**Output:** `FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md`, `screenshots/` (if Playwright available)

#### `/seo page <url>`

Deep single-page analysis: title, meta, headings, links, images, Schema, E-E-A-T, CWV.

```
/seo page https://example.com/about
```

---

### Technical SEO

#### `/seo technical <url>`

8-category audit: crawlability, indexability, security, URL structure, mobile, Core Web Vitals (LCP/INP/CLS), structured data, JS rendering.

#### `/seo schema <url>`

Detect existing schema (JSON-LD, Microdata, RDFa), validate against Google's requirements, identify missing opportunities, generate ready-to-use JSON-LD.

#### `/seo sitemap <url>` / `/seo sitemap generate`

Validate XML sitemaps (format, URLs, lastmod, coverage) or generate new ones with industry templates and quality gates.

#### `/seo hreflang <url>`

Validate self-refs, return tags, x-default, ISO codes. Generate correct hreflang implementations.

#### `/seo geo-technical <url>`

AI crawler management: GPTBot, ClaudeBot, PerplexityBot detection. llms.txt standard. SSR checks.

---

### Links

#### `/seo internal-links <url>`

Orphan pages, click depth analysis, anchor text optimization, link equity distribution.

#### `/seo backlinks profile <domain>` / `/seo backlinks gap <domain> <competitor>`

Backlink profile analysis, anchor text breakdown, toxic link detection, link gap opportunities. *(DataForSEO)*

#### `/seo redirects <url>`

Redirect chains, loops, 301/302 mixed signals, protocol issues, trailing slash consistency.

---

### Content

#### `/seo content-audit <url>`

E-E-A-T scoring (Experience 20%, Expertise 25%, Authoritativeness 25%, Trustworthiness 30%) + AI citability analysis.

#### `/seo images <url>`

Alt text quality, file sizes (flag >200KB), format recommendations (WebP/AVIF), responsive images, lazy loading, CLS prevention.

#### `/seo content-decay <url>`

Detect content losing rankings/traffic. Identifies pages needing refresh with priority list.

#### `/seo cannibalization <domain>`

Find multiple pages competing for the same keyword. Resolution strategies: merge, redirect, differentiate, or delete.

#### `/seo content-brief <keyword>`

Analyze SERP top 10 for target keyword, extract common topics, identify content gaps, create actionable brief.

#### `/seo content-writer`

SEO + AI optimized writing guidelines for content creation.

#### `/seo fake-freshness <url>`

Compare datePublished/dateModified against actual content age signals. Scores authenticity 0-100.

#### `/seo mobile-parity <url>`

Fetch desktop + mobile versions, compare meta tags, structured data, content, links, images. Scores parity 0-100.

#### `/seo discover <url>`

Google Discover optimization: clickbait title detection, content depth scoring, image readiness (1200px+), local relevance, sensationalism flags.

#### `/seo blog-pipeline <keyword>`

End-to-end SEO blog production: keyword research → SERP analysis → outline → draft → SEO optimization. Auto-detects CMS (Hugo, Next.js, WordPress, Astro, Gatsby). Outputs publish-ready markdown with front matter, schema JSON-LD, and SEO metadata.

Subcommands:
- `/seo blog-pipeline <keyword>` — Full pipeline
- `/seo blog-pipeline outline <keyword>` — Research + outline only
- `/seo blog-pipeline draft <outline-file>` — Draft from existing outline
- `/seo blog-pipeline optimize <draft-file>` — SEO-optimize existing draft

---

### Planning

#### `/seo plan <type>`

Types: `saas`, `local`, `ecommerce`, `publisher`, `agency`. Creates: competitive analysis, keyword strategy, content calendar, 4-phase implementation roadmap.

#### `/seo architecture <url>`

URL structure design, navigation planning, internal linking strategy, hub-and-spoke models.

---

### Programmatic SEO

#### `/seo programmatic plan`

Scale content: data sources, templates, quality gates, index control, thin content safeguards.

#### `/seo competitor-pages generate`

Generate X vs Y comparison pages, "alternatives to X" pages, feature matrices with schema.

---

### Monitoring

#### `/seo monitor overview` / `/seo monitor keywords`

Your site via Google Search Console: rankings, clicks, CTR, position changes. *(GSC)*

#### `/seo serp check <keyword>`

Live SERP check for any keyword: positions, SERP features, competitor domains. *(DataForSEO)*

#### `/seo ai-visibility domain <domain>`

Track mentions in ChatGPT, Claude, Perplexity, Gemini, AI Overview. *(DataForSEO)*

#### `/seo rank-tracking snapshot <domain>`

Current rankings, position history, ranking changes, trending keywords, position alerts. *(DataForSEO)*

#### `/seo competitive-tracking overview <domain> <competitor>`

Side-by-side comparison, shared keywords, competitor gains, threat detection, new content alerts. *(DataForSEO)*

#### `/seo cwv-analytics overview <url>`

CrUX real-user data, LCP subparts breakdown (TTFB + resource load delay + resource load time + render delay), INP diagnostics, CLS attribution, historical trends. *(Google API)*

---

### Data

#### `/seo keywords research <seed>` / `/seo keywords site <domain>` / `/seo keywords gap <domain> <competitor>`

Keyword ideas, search volume, difficulty, intent classification, trend analysis, site rankings, keyword gap. *(DataForSEO)*

---

### Advanced

#### `/seo semantic-search <url>`

Entity extraction, topical authority scoring, Knowledge Panel eligibility, entity relationship mapping, semantic content gap analysis.

#### `/seo content-localization <source-url> <localized-url>`

Translation quality scoring, cultural adaptation checks, locale-specific keyword analysis, content parity comparison, regional content gap detection.

#### `/seo blog-pipeline <keyword>`

End-to-end blog production pipeline. See Content section above for subcommands.

---

## Utility Scripts

| Script | Usage |
|--------|-------|
| `python3 scripts/health_check.py` | Validate installation, deps, credentials, skill integrity |
| `python3 scripts/interactive_setup.py` | Guided first-run configuration wizard |
| `python3 scripts/brand_mentions.py --brand "Name" --file response.txt` | Brand mention analysis from AI responses |
| `python3 scripts/fetch_page.py <url>` | Fetch page with SSRF prevention |
| `python3 scripts/parse_html.py <url>` | Extract SEO elements from HTML |
| `python3 scripts/capture_screenshot.py <url> --all` | Capture screenshots (requires Playwright) |
| `python3 scripts/analyze_visual.py <url> --json` | Visual analysis (requires Playwright) |
| `python3 scripts/telemetry.py report` | View local usage statistics |
| `python3 scripts/telemetry.py disable` | Opt out of local telemetry |
