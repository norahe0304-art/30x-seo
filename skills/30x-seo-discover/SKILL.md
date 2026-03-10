---
name: 30x-seo-discover
description: >
  Google Discover optimization checks. Detects clickbait titles, scores
  content depth, evaluates local relevance signals, and flags sensationalism.
  Use when user says "Discover optimization", "Google Discover", "Discover feed",
  "clickbait check", or "content depth scoring".
allowed-tools:
  - WebFetch
  - Read
maturity: beta
---

# Google Discover Optimization

Google Discover surfaces content to users based on interests, not search queries. Optimizing for Discover requires high-quality, engaging content without clickbait.

## Discover Eligibility Requirements

Content must meet ALL of these:
1. Indexed by Google
2. Meets Google News content policies
3. Has large, high-quality images (≥1200px wide, or use `max-image-preview:large`)
4. NOT a job posting, petition, form, code repository, or satire

## Analysis Checklist

### 1. Clickbait Title Detection

Flag titles that use manipulation tactics:

| Pattern | Example | Severity |
|---------|---------|----------|
| Curiosity gap | "You Won't Believe What Happened..." | High |
| Exaggeration | "The BEST Thing EVER Created" | Medium |
| False urgency | "Do This NOW Before It's Too Late" | High |
| Misleading | Title promises content that article doesn't deliver | Critical |
| Listicle bait | "10 Shocking Reasons..." | Medium |
| Emotional manipulation | "This Will Make You Cry" | High |
| ALL CAPS abuse | More than 1 word in caps | Low |

**Scoring:**
- 0 clickbait signals: +20 points
- 1-2 mild signals: +10 points
- 3+ signals or any Critical: -20 points

### 2. Content Depth Scoring

| Factor | Good (5pts) | Okay (3pts) | Poor (0pts) |
|--------|-------------|-------------|-------------|
| Word count | >1,500 | 800-1,500 | <800 |
| Original reporting | First-hand data/research | Aggregated with analysis | Pure aggregation |
| Expert sources | Named experts quoted | General authority cited | No sources |
| Visual content | Original images/charts | Stock + some original | Stock only |
| Timeliness | Breaking/trending topic | Evergreen value | Neither |
| Perspective | Unique angle | Standard coverage | Rehashed |

**Total: 30 points maximum**

### 3. Image Requirements

Discover heavily favors articles with compelling images:

- [ ] At least one image ≥1200px wide
- [ ] `<meta name="robots" content="max-image-preview:large">` present
- [ ] Images are original (not stock photos)
- [ ] Images have descriptive alt text
- [ ] Images relate to content (not generic headers)

**Scoring:**
- All checks pass: +20 points
- Image present but <1200px: +10 points
- No max-image-preview meta: -5 points
- No images or only stock: -10 points

### 4. Local Relevance Signals

For location-based Discover recommendations:

- [ ] Geographic entity mentions (city, region, country)
- [ ] Local event references
- [ ] Location-specific data or statistics
- [ ] `<meta name="geo.region">` or `<meta name="geo.placename">`
- [ ] Schema with `contentLocation` or `locationCreated`

**Scoring:**
- Strong local signals: +10 points
- Some signals: +5 points
- No local relevance: 0 points (neutral, not penalized)

### 5. Sensationalism Flags

Content that crosses from engaging to sensational:

| Flag | Description |
|------|-------------|
| Fear-mongering | Creating unnecessary panic or fear |
| Outrage bait | Designed to provoke anger |
| Conspiracy signals | Unsubstantiated claims, "they don't want you to know" |
| Health misinformation | Unverified medical claims |
| Financial hype | "Get rich quick" or crypto pump signals |

**Any sensationalism flag: -20 points**

## Overall Discover Score

| Score | Rating | Discover Potential |
|-------|--------|--------------------|
| 80-100 | Excellent | High likelihood of Discover inclusion |
| 60-79 | Good | Moderate potential, optimize weak areas |
| 40-59 | Fair | Unlikely without significant improvements |
| 0-39 | Poor | Not suitable for Discover |

**Maximum: 100 points** (Clickbait 20 + Depth 30 + Images 20 + Engagement 20 + Local 10)

## Output Format

```
## Discover Optimization Report

**URL**: [url]
**Discover Score**: [0-100] / 100

### Title Analysis
- Title: "[title text]"
- Clickbait signals: [list or "none detected"]
- Title score: [x] / 20

### Content Depth
- Word count: [n]
- Original reporting: [Yes/No/Partial]
- Expert sources: [Yes/No]
- Depth score: [x] / 30

### Image Readiness
- Largest image: [width]px
- max-image-preview: [present/missing]
- Image score: [x] / 20

### Engagement Signals
- Topic timeliness: [Breaking/Evergreen/Stale]
- Unique perspective: [Yes/No]
- Engagement score: [x] / 20

### Local Relevance
- Geo signals: [list or "none"]
- Local score: [x] / 10

### Sensationalism Check
- Flags: [list or "none"]

### Recommendations
- [prioritized actions to improve Discover potential]
```
