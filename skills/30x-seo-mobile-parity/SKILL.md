---
name: 30x-seo-mobile-parity
description: >
  Compare mobile vs desktop content parity for mobile-first indexing.
  Checks meta tags, structured data, content completeness, and rendering
  differences. Use when user says "mobile parity", "mobile-first indexing",
  "mobile vs desktop", "content parity", or "mobile SEO check".
allowed-tools:
  - WebFetch
  - Read
maturity: beta
---

# Mobile Content Parity Check

Google uses mobile-first indexing — the mobile version of your page is what gets indexed. Content or metadata missing from mobile = invisible to Google.

## Analysis Method

### Step 1: Fetch Both Versions

Use WebFetch twice with different User-Agent headers:

**Desktop fetch:**
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

**Mobile fetch:**
```
User-Agent: Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36
```

### Step 2: Compare Elements

Check each category for parity:

#### Meta Tags
| Element | Desktop | Mobile | Parity? |
|---------|---------|--------|---------|
| `<title>` | | | |
| `<meta description>` | | | |
| `<meta robots>` | | | |
| `<link rel="canonical">` | | | |
| `<meta viewport>` | N/A | Required | |

**Critical**: If `<meta name="robots">` differs (e.g., mobile has `noindex`), the page may be deindexed.

#### Structured Data
- Count JSON-LD blocks: desktop vs mobile
- Compare `@type` values present in each
- Flag any schema present on desktop but missing on mobile

#### Content
- Compare H1 text
- Compare heading count (H2-H6)
- Estimate word count difference (>20% gap = problem)
- Check for `display:none` or `hidden` content on mobile that exists on desktop
- Verify images are present (not lazy-loaded into oblivion)

#### Links
- Compare internal link count
- Check if navigation links differ significantly
- Verify footer links present on both

#### Images
- Compare `<img>` count
- Check for `alt` text parity
- Verify `srcset` / responsive image usage on mobile

### Step 3: Score Parity

| Score | Rating | Risk |
|-------|--------|------|
| 95-100 | Excellent parity | No risk |
| 80-94 | Good parity | Low risk |
| 60-79 | Partial parity | Medium risk — content may be under-indexed |
| 0-59 | Poor parity | High risk — likely indexing issues |

### Scoring Rules

**Critical (immediate fix):**
- `-30` Different `<meta robots>` directives
- `-25` Structured data missing on mobile
- `-20` H1 missing or different on mobile
- `-20` >50% content hidden on mobile

**High (fix within 1 week):**
- `-15` >30% fewer internal links on mobile
- `-10` Title tag differs
- `-10` Canonical differs

**Medium (fix within 1 month):**
- `-5` >20% word count difference
- `-5` Images missing alt text on mobile only
- `-3` per missing heading level on mobile

## Common Problems

### 1. Accordion/Tab Content
Content inside collapsed accordions may not be indexed. Google says it indexes hidden content, but collapsed content gets reduced weight.

**Fix**: Use `<details>` element or ensure content is in DOM (not lazy-loaded via JS).

### 2. Hamburger Menu Links
Navigation links hidden behind hamburger menus are still crawled, but may receive less link equity.

**Fix**: Ensure critical category/pillar page links are in the visible mobile content, not just navigation.

### 3. Separate Mobile Site (m.example.com)
If using a separate mobile site:
- Verify `rel="alternate"` and `rel="canonical"` are correctly paired
- Content should match desktop version
- Consider migrating to responsive design

## Output Format

```
## Mobile Parity Report

**URL**: [url]
**Parity Score**: [0-100] / 100

### Element Comparison
| Element | Desktop | Mobile | Match? |
|---------|---------|--------|--------|
| Title | "..." | "..." | Yes/No |
| Meta Description | "..." | "..." | Yes/No |
| H1 | "..." | "..." | Yes/No |
| JSON-LD blocks | 3 | 2 | No — missing Product |
| Word count | 1,850 | 1,200 | No — 35% gap |
| Internal links | 45 | 28 | No — 38% fewer |
| Images | 12 | 10 | Partial |

### Critical Issues
- [list]

### Recommendations
- [prioritized actions]
```
