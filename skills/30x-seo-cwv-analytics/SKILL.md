---
name: 30x-seo-cwv-analytics
description: >
  Core Web Vitals real-user analytics using CrUX API and PageSpeed Insights.
  Analyze LCP subparts (TTFB, resource load delay, resource load time, render delay),
  INP diagnostics, CLS element attribution, and field vs lab data comparison.
  Use when user says "CWV analytics", "Core Web Vitals data", "CrUX data",
  "LCP subparts", "INP analysis", "real user metrics", or "field data".
allowed-tools:
  - Bash
  - Read
maturity: beta
---

# Core Web Vitals Analytics

Real-user performance analysis using Chrome User Experience Report (CrUX) data and PageSpeed Insights API.

## API Configuration

### CrUX API (free, requires Google API key)

```bash
CRUX_KEY="YOUR_GOOGLE_API_KEY"
```

### PageSpeed Insights API (free, same key)

```bash
PSI_KEY="YOUR_GOOGLE_API_KEY"
```

Store at `~/.config/google/api_key` or pass directly.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo cwv-analytics overview <url>` | Full CWV report with field + lab data |
| `/seo cwv-analytics lcp <url>` | LCP subparts breakdown |
| `/seo cwv-analytics inp <url>` | INP diagnostics and long task analysis |
| `/seo cwv-analytics cls <url>` | CLS element attribution |
| `/seo cwv-analytics compare <url1> <url2>` | Side-by-side CWV comparison |
| `/seo cwv-analytics trend <origin>` | Historical CWV trend for an origin |

---

## 1. Full CWV Overview

Get complete Core Web Vitals assessment combining field (CrUX) and lab (Lighthouse) data.

### CrUX API — Field Data (real users)

```bash
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/page",
    "metrics": [
      "largest_contentful_paint",
      "interaction_to_next_paint",
      "cumulative_layout_shift",
      "experimental_time_to_first_byte",
      "first_contentful_paint",
      "round_trip_time",
      "form_factors"
    ]
  }'
```

### PageSpeed Insights — Lab Data

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/page&key=$PSI_KEY&strategy=mobile&category=performance"
```

### CWV Thresholds (2026)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP | ≤200ms | 200ms–500ms | >500ms |
| CLS | ≤0.1 | 0.1–0.25 | >0.25 |

**IMPORTANT**: Google evaluates the **75th percentile (p75)** of page visits.

### Overview Report Format

```
## Core Web Vitals — example.com/page

### Field Data (CrUX — real users, p75)
| Metric | Value | Status | Distribution |
|--------|-------|--------|-------------|
| LCP | 2.1s | ✅ Good | 78% good, 15% NI, 7% poor |
| INP | 156ms | ✅ Good | 82% good, 12% NI, 6% poor |
| CLS | 0.08 | ✅ Good | 85% good, 10% NI, 5% poor |
| TTFB | 420ms | ⚠️ Needs Improvement | — |
| FCP | 1.4s | ✅ Good | — |

### Lab Data (Lighthouse)
| Metric | Value | Score |
|--------|-------|-------|
| Performance Score | 85 | — |
| LCP | 2.3s | — |
| TBT (proxy for INP) | 180ms | — |
| CLS | 0.05 | — |
| Speed Index | 3.2s | — |

### Field vs Lab Delta
| Metric | Field | Lab | Gap | Explanation |
|--------|-------|-----|-----|-------------|
| LCP | 2.1s | 2.3s | +0.2s | Lab slightly pessimistic |
| CLS | 0.08 | 0.05 | -0.03 | Ads/dynamic content in field |

### Overall: ✅ Passing CWV (all three green at p75)
```

---

## 2. LCP Subparts Breakdown

Decompose LCP into its four components for targeted optimization.

### LCP Subparts (available in CrUX since February 2025)

```bash
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/page",
    "metrics": [
      "largest_contentful_paint",
      "experimental_time_to_first_byte"
    ]
  }'
```

Combine with PageSpeed Insights for element-level details.

### LCP Subpart Model

```
Total LCP = TTFB + Resource Load Delay + Resource Load Time + Element Render Delay
```

| Subpart | What It Measures | Good Target |
|---------|-----------------|-------------|
| **TTFB** | Server response time | <800ms |
| **Resource Load Delay** | Time from TTFB to start loading LCP resource | <100ms |
| **Resource Load Time** | Time to download LCP resource (image/font) | <800ms |
| **Element Render Delay** | Time from resource loaded to rendered | <100ms |

### LCP Subparts Report Format

```
## LCP Subparts — example.com/page
**Total LCP**: 2.1s (p75)

| Subpart | Value | % of LCP | Status | Fix |
|---------|-------|----------|--------|-----|
| TTFB | 620ms | 30% | ⚠️ | CDN, server optimization |
| Resource Load Delay | 80ms | 4% | ✅ | — |
| Resource Load Time | 950ms | 45% | ⚠️ | Compress image, use AVIF |
| Element Render Delay | 450ms | 21% | ⚠️ | Remove render-blocking JS |

### LCP Element
- Type: `<img>`
- Source: `/images/hero-banner.jpg`
- Size: 850KB (should be <200KB)
- Format: JPEG (convert to AVIF/WebP)
- Preloaded: No ❌ (add `<link rel="preload">`)

### Priority Fixes
1. **Resource Load Time (45%)**: Compress hero image from 850KB to <200KB, convert to AVIF
2. **TTFB (30%)**: Deploy CDN edge caching, target <200ms
3. **Element Render Delay (21%)**: Defer non-critical JS, inline critical CSS
```

---

## 3. INP Diagnostics

Analyze Interaction to Next Paint issues — the most challenging CWV metric.

### INP Data from CrUX

```bash
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/page",
    "metrics": ["interaction_to_next_paint"]
  }'
```

### INP Breakdown Model

```
INP = Input Delay + Processing Time + Presentation Delay
```

| Component | What It Measures | Common Causes |
|-----------|-----------------|---------------|
| **Input Delay** | Time from interaction to handler start | Long tasks blocking main thread |
| **Processing Time** | Time in event handler | Heavy JS computation, DOM manipulation |
| **Presentation Delay** | Time from handler end to next paint | Large layout recalculations, forced reflows |

### Common INP Offenders

| Issue | Impact | Fix |
|-------|--------|-----|
| Third-party scripts | Block main thread | Defer, use web workers |
| Large DOM (>1,500 nodes) | Slow layout | Virtualize lists, simplify structure |
| Synchronous XHR | Blocks thread | Use async fetch() |
| Heavy event handlers | Long processing | Debounce, requestAnimationFrame |
| Excessive DOM reads in handlers | Forced reflows | Batch reads before writes |
| Unoptimized React re-renders | Cascading updates | useMemo, React.memo, virtualize |

### INP Report Format

```
## INP Analysis — example.com/page
**INP (p75)**: 245ms ⚠️ Needs Improvement

### Distribution
- Good (≤200ms): 62%
- Needs Improvement (200-500ms): 28%
- Poor (>500ms): 10%

### Likely Causes
1. **Third-party scripts**: 4 blocking scripts detected (analytics, chat widget, ads)
2. **DOM Size**: 2,340 nodes (above 1,500 threshold)
3. **Event handlers**: Click handlers with synchronous operations

### Recommendations
1. Defer non-critical third-party scripts: move analytics to `requestIdleCallback`
2. Reduce DOM complexity: virtualize product list (currently 200+ items)
3. Optimize click handlers: use `requestAnimationFrame` for visual updates
4. Consider Web Workers for data processing tasks

### Target: <200ms (need 45ms improvement)
```

---

## 4. CLS Element Attribution

Identify which elements cause layout shifts.

Use PageSpeed Insights for CLS attribution:

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/page&key=$PSI_KEY&strategy=mobile&category=performance" \
  | jq '.lighthouseResult.audits["layout-shift-elements"]'
```

### CLS Report Format

```
## CLS Analysis — example.com/page
**CLS (p75)**: 0.18 ⚠️ Needs Improvement

### Shift-Causing Elements
| Element | Shift Score | Cause |
|---------|-----------|-------|
| `.ad-banner` | 0.08 | Dynamically injected ad |
| `img.hero` | 0.06 | Missing width/height |
| `.cookie-banner` | 0.04 | Late-loading overlay |

### Fixes
1. **Ad banner**: Reserve space with `min-height: 250px` on container
2. **Hero image**: Add `width="1200" height="630"` attributes
3. **Cookie banner**: Use fixed positioning, don't push content
```

---

## 5. Side-by-Side Comparison

Compare CWV between two URLs (e.g., your page vs competitor, or before/after).

### Comparison Report Format

```
## CWV Comparison

| Metric | Page A | Page B | Winner |
|--------|--------|--------|--------|
| LCP | 2.1s ✅ | 3.8s ⚠️ | Page A |
| INP | 245ms ⚠️ | 156ms ✅ | Page B |
| CLS | 0.08 ✅ | 0.22 ⚠️ | Page A |
| Performance Score | 82 | 68 | Page A |
| TTFB | 420ms | 180ms | Page B |
```

---

## 6. Historical CWV Trend

Track CWV changes over time for an origin (domain-level).

```bash
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "https://example.com",
    "metrics": [
      "largest_contentful_paint",
      "interaction_to_next_paint",
      "cumulative_layout_shift"
    ]
  }'
```

Returns 25 data points (weekly, ~6 months of history).

### Trend Report Format

```
## CWV Trend — example.com (last 6 months)

### LCP (p75)
2.8s → 2.5s → 2.3s → 2.1s → 2.0s → 1.9s  ↓ Improving

### INP (p75)
310ms → 280ms → 245ms → 220ms → 200ms → 190ms  ↓ Improving

### CLS (p75)
0.15 → 0.12 → 0.10 → 0.09 → 0.08 → 0.08  → Stable (passing)

### Assessment
- All metrics trending positive
- LCP improved 32% (2.8s → 1.9s)
- INP crossed "Good" threshold in February
- CLS stable and passing since December
```

---

## Integration With Other Skills

- Poor LCP → `/seo images` for image optimization
- Poor INP → `/seo technical` for JS analysis
- Poor CLS → `/seo page` for element analysis
- Competitor has better CWV → `/seo competitive-tracking` + this skill for comparison

## Notes

- **CrUX data requires sufficient traffic** — low-traffic pages may not have field data
- **CrUX updates monthly** (28-day rolling window)
- **Lab ≠ Field** — always prioritize CrUX field data for ranking impact
- **Mobile vs Desktop** — Google uses mobile CWV for ranking. Add `"formFactor": "PHONE"` to CrUX queries

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
