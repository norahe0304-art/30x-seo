---
name: 30x-seo-rank-tracking
description: >
  Historical rank tracking and position change alerts using DataForSEO.
  Track keyword positions over time, detect ranking gains/losses, identify
  trending keywords, and set up position change thresholds. Use when user says
  "rank tracking", "position history", "ranking changes", "rank alerts",
  "keyword position over time", or "SERP history".
allowed-tools:
  - Bash
  - Read
maturity: beta
---

# Rank Tracking

Track keyword rankings over time, detect position changes, and alert on significant movements.

## API Configuration

```bash
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo rank-tracking snapshot <domain>` | Current rankings for all tracked keywords |
| `/seo rank-tracking history <domain> <keyword>` | Position history for a specific keyword |
| `/seo rank-tracking changes <domain>` | Detect ranking gains and losses |
| `/seo rank-tracking trending <domain>` | Keywords with strongest upward momentum |
| `/seo rank-tracking alerts <domain>` | Keywords that crossed alert thresholds |

---

## 1. Current Rankings Snapshot

Get current keyword positions for a domain.

**Input**: domain name
**Output**: All ranked keywords with current position, URL, SERP features

```bash
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "example.com",
    "language_code": "en",
    "location_code": 2840,
    "limit": 100,
    "order_by": ["keyword_data.keyword_info.search_volume,desc"],
    "filters": ["ranked_serp_element.serp_item.rank_group", "<=", 20]
  }]'
```

### Snapshot Report Format

```
## Rankings Snapshot — example.com
**Date**: 2026-03-10 | **Keywords in Top 20**: 142

| Keyword | Position | URL | Volume | SERP Features |
|---------|----------|-----|--------|---------------|
| [kw] | #3 | /page | 2,400 | Featured Snippet |
| ... | ... | ... | ... | ... |

### Distribution
- Top 3: 12 keywords
- Top 10: 45 keywords
- Top 20: 142 keywords
```

---

## 2. Position History

Track position changes for a specific keyword over time.

**Input**: domain + keyword
**Output**: Historical positions with dates and URL changes

```bash
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/historical_serps/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "keyword": "best project management software",
    "language_code": "en",
    "location_code": 2840
  }]'
```

### Cross-reference with domain:

After getting historical SERPs, search for target domain in each snapshot to build position timeline.

### History Report Format

```
## Position History — "best project management software"
**Domain**: example.com | **Period**: Last 6 months

| Date | Position | URL | Change |
|------|----------|-----|--------|
| 2026-03-01 | #5 | /tools/pm | — |
| 2026-02-01 | #7 | /tools/pm | +2 ↑ |
| 2026-01-01 | #12 | /blog/pm-guide | +5 ↑ |
| 2025-12-01 | #18 | /blog/pm-guide | — |
| 2025-11-01 | #15 | /blog/pm-guide | -3 ↓ |
| 2025-10-01 | #22 | /blog/pm-guide | +7 ↑ |

### Trend: ↑ Improving (22 → 5 over 6 months)
### URL Change: Ranking shifted from /blog/pm-guide to /tools/pm in January
```

---

## 3. Ranking Changes Detection

Compare current rankings against a baseline period to find gains and losses.

**Input**: domain
**Output**: Keywords that moved significantly (±5 positions or more)

```bash
# Get current ranked keywords
curl -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "example.com",
    "language_code": "en",
    "location_code": 2840,
    "limit": 500
  }]'
```

Then compare with historical data from `/seo rank-tracking history`.

### Change Detection Thresholds

| Change | Category | Action |
|--------|----------|--------|
| ≥10 positions up | **Big Win** | Analyze what worked, replicate |
| 5-9 positions up | **Gain** | Monitor, continue optimization |
| ±4 positions | **Stable** | No action needed |
| 5-9 positions down | **Loss** | Investigate, check for issues |
| ≥10 positions down | **Alert** | Urgent review — possible penalty or algorithm hit |
| Dropped out of Top 100 | **Critical** | Immediate investigation |

### Changes Report Format

```
## Ranking Changes — example.com
**Period**: Last 30 days

### 🚀 Big Wins (≥10 pos up)
| Keyword | Old | New | Change | Volume |
|---------|-----|-----|--------|--------|
| [kw] | #25 | #8 | +17 ↑ | 3,200 |

### 📈 Gains (5-9 pos up)
| Keyword | Old | New | Change | Volume |
|---------|-----|-----|--------|--------|

### 📉 Losses (5-9 pos down)
| Keyword | Old | New | Change | Volume |
|---------|-----|-----|--------|--------|

### 🚨 Alerts (≥10 pos down)
| Keyword | Old | New | Change | Volume |
|---------|-----|-----|--------|--------|

### Summary
- Total keywords tracked: 245
- Improved: 67 (27%)
- Stable: 145 (59%)
- Declined: 33 (13%)
- Net trend: ↑ Positive
```

---

## 4. Trending Keywords

Identify keywords with the strongest upward momentum.

**Input**: domain
**Output**: Keywords sorted by positive position change velocity

### Momentum Score

Calculate momentum as weighted position change over time:

```
momentum = (pos_3mo_ago - pos_current) × log(search_volume)
```

Higher momentum = keyword improving fast with meaningful volume.

### Trending Report Format

```
## Trending Keywords — example.com

| Keyword | Current | 30d ago | 90d ago | Momentum | Volume |
|---------|---------|---------|---------|----------|--------|
| [kw] | #4 | #12 | #35 | 85.2 | 5,400 |
| [kw] | #7 | #15 | #28 | 62.1 | 2,100 |

### Opportunities
- Keywords approaching Top 3 (currently #4-#10 with upward trend): [list]
- Keywords entering first page (currently #8-#15 with momentum): [list]
```

---

## 5. Position Alerts

Define thresholds and alert on keywords that cross them.

### Default Alert Rules

| Rule | Trigger | Severity |
|------|---------|----------|
| Lost Top 3 | Was #1-3, now #4+ | Critical |
| Lost First Page | Was #1-10, now #11+ | High |
| Lost Top 20 | Was #1-20, now #21+ | Medium |
| Entered Top 3 | Was #4+, now #1-3 | Positive |
| Entered First Page | Was #11+, now #1-10 | Positive |
| New Ranking | Not ranked before, now in Top 50 | Info |

### Alerts Report Format

```
## Ranking Alerts — example.com

### 🔴 Critical
| Keyword | Was | Now | Volume | Ranking URL |
|---------|-----|-----|--------|-------------|
| [kw] | #2 | #8 | 12,000 | /page |

### 🟡 Warning
| Keyword | Was | Now | Volume | Ranking URL |
|---------|-----|-----|--------|-------------|

### 🟢 Positive
| Keyword | Was | Now | Volume | Ranking URL |
|---------|-----|-----|--------|-------------|

### Recommended Actions
1. [Critical keyword]: Check page for content changes, lost backlinks, or competitor updates
2. [Positive keyword]: Document what's working, apply to similar pages
```

---

## Best Practices

### Monitoring Cadence
- **Daily**: Top 10 high-value keywords (if DataForSEO budget allows)
- **Weekly**: Full keyword set position check
- **Monthly**: Comprehensive trend analysis with momentum scoring

### Pairing With Other Skills
- Lost rankings → `/seo content-audit` to check page quality
- New ranking opportunities → `/seo content-brief` to create content
- Position volatility → `/seo technical` to check indexing issues
- Competitor overtook you → `/seo competitive-tracking` for analysis

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
