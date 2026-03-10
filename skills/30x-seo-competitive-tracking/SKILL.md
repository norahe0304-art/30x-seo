---
name: 30x-seo-competitive-tracking
description: >
  Automated competitor SERP monitoring using DataForSEO. Track competitor
  ranking changes, detect new content, compare domain authority trends,
  and identify when competitors gain or lose positions on your target keywords.
  Use when user says "competitor tracking", "competitor monitoring",
  "competitor rankings", "competitive analysis", or "track competitors".
allowed-tools:
  - Bash
  - Read
maturity: beta
---

# Competitive Tracking

Monitor competitor SERP movements, detect strategy shifts, and identify threats and opportunities.

## API Configuration

```bash
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo competitive-tracking overview <domain> <competitor>` | Side-by-side domain comparison |
| `/seo competitive-tracking keywords <domain> <competitor>` | Shared keyword analysis |
| `/seo competitive-tracking gains <competitor>` | Keywords competitor recently gained |
| `/seo competitive-tracking threats <domain> <competitor>` | Keywords where competitor is overtaking you |
| `/seo competitive-tracking new-content <competitor>` | Detect competitor's newly ranked pages |

---

## 1. Domain Comparison Overview

Side-by-side metrics comparison between your domain and a competitor.

**Input**: your domain + competitor domain
**Output**: Comparative metrics dashboard

```bash
# Your domain metrics
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "example.com",
    "language_code": "en",
    "location_code": 2840
  }]'

# Competitor metrics (same endpoint)
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "competitor.com",
    "language_code": "en",
    "location_code": 2840
  }]'
```

### Overview Report Format

```
## Competitive Overview

| Metric | example.com | competitor.com | Delta |
|--------|-------------|----------------|-------|
| Domain Rank | 450 | 520 | -70 |
| Organic Keywords | 1,234 | 2,567 | -1,333 |
| Organic Traffic (est.) | 45,000 | 78,000 | -33,000 |
| Top 3 Keywords | 45 | 89 | -44 |
| Top 10 Keywords | 156 | 312 | -156 |
| Backlink Domains | 890 | 1,450 | -560 |

### Assessment
- Competitor has [X]% more keyword coverage
- Estimated organic traffic gap: [N] visits/month
- Key advantage area: [area]
```

---

## 2. Shared Keyword Analysis

Find keywords where both domains rank and compare positions.

**Input**: your domain + competitor domain
**Output**: Head-to-head keyword comparison

```bash
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target1": "example.com",
    "target2": "competitor.com",
    "language_code": "en",
    "location_code": 2840,
    "intersections": true,
    "limit": 100,
    "order_by": ["keyword_data.keyword_info.search_volume,desc"]
  }]'
```

### Shared Keywords Report

```
## Shared Keywords — example.com vs competitor.com

### You're Winning (your position < competitor)
| Keyword | You | Them | Gap | Volume |
|---------|-----|------|-----|--------|
| [kw] | #3 | #8 | +5 | 4,500 |

### They're Winning (their position < yours)
| Keyword | You | Them | Gap | Volume |
|---------|-----|------|-----|--------|
| [kw] | #12 | #4 | -8 | 6,200 |

### Close Battles (within ±3 positions)
| Keyword | You | Them | Gap | Volume |
|---------|-----|------|-----|--------|

### Summary
- Shared keywords: 345
- You win: 123 (36%)
- They win: 178 (52%)
- Close battles: 44 (13%)
```

---

## 3. Competitor Gains Detection

Identify keywords where competitor recently improved rankings.

**Input**: competitor domain
**Output**: Keywords with recent position improvements

Use the ranked_keywords endpoint and compare against historical data:

```bash
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "competitor.com",
    "language_code": "en",
    "location_code": 2840,
    "limit": 200,
    "order_by": ["ranked_serp_element.serp_item.rank_group,asc"],
    "filters": ["ranked_serp_element.serp_item.rank_group", "<=", 10]
  }]'
```

Cross-reference with historical SERPs to detect recent gains.

### Gains Report Format

```
## Competitor Gains — competitor.com
**Period**: Last 30 days

### New First-Page Rankings
| Keyword | Position | Volume | Ranking URL |
|---------|----------|--------|-------------|
| [kw] | #6 | 3,400 | /new-page |

### Significant Improvements
| Keyword | Old | New | Change | Volume |
|---------|-----|-----|--------|--------|
| [kw] | #18 | #5 | +13 ↑ | 5,100 |

### Content Strategy Signal
- New URLs appearing: [list of new ranking URLs]
- Topics competitor is investing in: [analysis]
- Estimated new traffic from gains: [number]
```

---

## 4. Threat Detection

Keywords where competitor is actively overtaking your positions.

**Input**: your domain + competitor domain
**Output**: Keywords where the gap is closing or has reversed

### Threat Levels

| Scenario | Threat Level | Action |
|----------|-------------|--------|
| Competitor entered Top 10, you're #1-5 | **Watch** | Monitor weekly |
| Competitor within 3 positions of you | **Moderate** | Optimize your page |
| Competitor just overtook you | **High** | Immediate content refresh |
| Competitor #1-3, you dropped to #10+ | **Critical** | Content overhaul or new approach |

### Threat Report Format

```
## Competitive Threats — competitor.com → example.com

### 🔴 Critical Threats
| Keyword | You | Them | Volume | Your URL |
|---------|-----|------|--------|----------|
| [kw] | #15 | #2 | 8,000 | /page |

### 🟡 High Threats
| Keyword | You | Them | Volume | Your URL |
|---------|-----|------|--------|----------|
| [kw] | #6 | #4 | 5,500 | /page |

### 🟠 Moderate Threats
| Keyword | You | Them | Gap | Volume |
|---------|-----|------|-----|--------|

### Recommended Actions
1. [Critical]: Analyze competitor.com/page — what are they doing differently?
2. [High]: Run /seo content-audit on your URL, identify gaps
3. [Moderate]: Add to weekly monitoring list
```

---

## 5. New Content Detection

Detect competitor's newly ranked pages (URLs that weren't ranking 30 days ago).

**Input**: competitor domain
**Output**: New ranking URLs with keywords

```bash
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "competitor.com",
    "language_code": "en",
    "location_code": 2840,
    "limit": 500,
    "order_by": ["ranked_serp_element.serp_item.rank_group,asc"]
  }]'
```

Group results by URL. New URLs (not seen in previous snapshots) indicate new content.

### New Content Report Format

```
## Competitor New Content — competitor.com
**Period**: Last 30 days

### New Pages Detected
| URL | Keywords Ranked | Best Position | Top Keyword | Volume |
|-----|----------------|---------------|-------------|--------|
| /blog/new-post | 12 | #4 | "keyword" | 3,200 |

### Content Strategy Insights
- Topics competitor is targeting: [list]
- Content types: [blog posts, landing pages, comparison pages]
- Average keywords per new page: [n]

### Response Recommendations
1. Do you have content on "[topic]"? If not → /seo content-brief "[keyword]"
2. Your existing page on "[topic]" could be refreshed → /seo content-decay
3. Competitor used comparison format → /seo competitor-pages generate
```

---

## Monitoring Schedule

| Check | Frequency | Trigger Action |
|-------|-----------|----------------|
| Domain overview comparison | Monthly | Flag if competitor closes gap by >10% |
| Shared keyword positions | Weekly | Alert on position reversals |
| Competitor gains | Weekly | Investigate new Top 10 rankings |
| Threat detection | Bi-weekly | Prioritize pages needing defense |
| New content detection | Weekly | Create response content plan |

## Integration With Other Skills

- Threats detected → `/seo content-audit` your threatened pages
- Competitor new content → `/seo content-brief` to plan response
- Lost positions → `/seo rank-tracking` for your historical context
- Competitor backlink growth → `/seo backlinks gap` to find link opportunities

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
