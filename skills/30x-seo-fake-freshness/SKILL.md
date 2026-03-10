---
name: 30x-seo-fake-freshness
description: >
  Detect fake freshness — pages with updated dates but unchanged content.
  Compares datePublished/dateModified in schema and visible HTML against
  actual content modification signals. Use when user says "fake freshness",
  "date manipulation", "updated date check", or "content freshness audit".
allowed-tools:
  - WebFetch
  - Read
maturity: beta
---

# Fake Freshness Detection

Detect pages that update their published/modified dates without meaningfully changing content. Google's freshness algorithms penalize this practice.

## Detection Method

### Step 1: Extract Date Signals

Fetch the page via WebFetch and extract all date indicators:

**Schema.org dates:**
- `datePublished` in JSON-LD or Microdata
- `dateModified` in JSON-LD or Microdata
- `dateCreated` if present

**HTML visible dates:**
- `<time>` elements with datetime attributes
- Visible text like "Updated:", "Last modified:", "Published:"
- `<meta>` tags: `article:published_time`, `article:modified_time`

**HTTP headers:**
- `Last-Modified` header (from WebFetch response)

### Step 2: Analyze Content Age Signals

Look for indicators that content has NOT actually been updated:

| Signal | Indicates Stale Content |
|--------|------------------------|
| Outdated statistics/years | "In 2023, the market..." on a "2026" article |
| Dead links | External links returning 404 |
| Deprecated references | Mentioning discontinued products/services |
| Screenshot age | Old UI screenshots of tools/platforms |
| Comment dates | Reader comments much older than "modified" date |
| Wayback-style markers | Content structure unchanged despite date bump |

### Step 3: Score Freshness Authenticity

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Genuinely fresh | No action needed |
| 70-89 | Mostly fresh, minor stale signals | Flag for review |
| 50-69 | Suspicious freshness | Recommend content update |
| 0-49 | Likely fake freshness | Urgent: update content or revert date |

### Scoring Criteria

**Deduct points for:**
- `-20` dateModified > 6 months newer than any content signal
- `-15` Statistics or data references older than dateModified year
- `-10` per dead outbound link
- `-10` References to deprecated/discontinued items
- `-5` No visible "what changed" indicator (changelog, update note)

**Bonus points for:**
- `+10` Explicit "Update:" or "Editor's note:" sections
- `+10` Statistics matching current year
- `+5` Changelog or revision history visible
- `+5` dateModified and Last-Modified header within 7 days

## Red Flags

Flag immediately if:
1. `dateModified` is today/yesterday but content references are 1+ year old
2. `dateModified` changes on every page load (dynamic date injection)
3. `datePublished` is backdated (published date set in the future then moved back)
4. Multiple pages modified on the exact same date (bulk date bump)

## Output Format

```
## Freshness Authenticity Report

**URL**: [url]
**Freshness Score**: [0-100] / 100

### Date Signals Found
| Source | Date | Type |
|--------|------|------|
| JSON-LD datePublished | 2025-03-15 | Schema |
| JSON-LD dateModified | 2026-03-01 | Schema |
| Last-Modified header | 2026-03-01 | HTTP |

### Stale Content Signals
- [list of detected signals]

### Verdict
[Genuine / Suspicious / Fake Freshness]

### Recommendations
- [specific actions]
```
