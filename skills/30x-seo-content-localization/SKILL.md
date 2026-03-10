---
name: 30x-seo-content-localization
description: >
  Multi-language content quality optimization beyond hreflang. Checks translation
  quality, cultural adaptation, locale-specific keyword usage, local entity references,
  and regional content gaps. Use when user says "content localization", "translation SEO",
  "multi-language content", "localized content quality", "international content",
  or "locale optimization".
allowed-tools:
  - WebFetch
  - Read
maturity: experimental
---

# Content Localization Optimization

Go beyond hreflang technical setup — optimize the actual content quality for each locale. Poor translations and missing cultural adaptation are the top reasons international SEO fails.

> **Note**: For hreflang tag validation, use `/seo hreflang`. This skill focuses on content quality per locale.

## Analysis Method

Fetch both the source language page and the localized page via WebFetch. Compare content quality, not just technical tags.

## 1. Translation Quality Signals

### Red Flags (machine translation artifacts)

| Signal | Severity | Example |
|--------|----------|---------|
| Untranslated strings | Critical | English UI text in a Japanese page |
| Mixed languages | High | Sentences switching between languages |
| Literal translations | High | Idioms translated word-for-word |
| Wrong number format | Medium | US format ($1,000.00) on German page (should be 1.000,00 €) |
| Wrong date format | Medium | MM/DD/YYYY on European locale |
| Wrong currency | High | USD prices on a .de page |
| Placeholder text | Critical | [TRANSLATE], lorem ipsum, TODO |

### Quality Score

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Native quality | Content reads as originally written in this language |
| 70-89 | Good localization | Minor issues, overall natural |
| 50-69 | Adequate | Understandable but clearly translated |
| 0-49 | Poor | Machine translation artifacts, may harm trust |

## 2. Cultural Adaptation Check

Beyond translation — is the content culturally appropriate?

### Adaptation Checklist

| Element | Check | Example |
|---------|-------|---------|
| Images | Culturally appropriate? | Stock photos match target audience ethnicity |
| Examples | Locally relevant? | Case studies from target market |
| Testimonials | From local customers? | Local company names, not just US brands |
| Measurements | Converted to local units? | Metric vs imperial |
| Legal/Compliance | Meets local requirements? | GDPR notice for EU, specific disclaimers |
| Payment methods | Local options shown? | iDEAL for NL, Pix for BR |
| Phone numbers | Local format? | Country code, local number format |
| Address | Local format? | Postal code position varies by country |

## 3. Locale-Specific Keyword Analysis

Check if the page uses the right keywords for the target market, not just translated versions.

### Common Mistakes

| Source (EN-US) | Bad Translation | Correct Localization |
|----------------|----------------|---------------------|
| "apartment" | "apartment" (UK) | "flat" (UK) |
| "cell phone" | "cell phone" (ES) | "teléfono móvil" / "celular" (latam) |
| "pants" | "pants" (UK) | "trousers" (UK) |
| "vacation" | "vacation" (UK) | "holiday" (UK) |

### What to Check

- [ ] H1 uses locale-preferred keyword (not literal translation)
- [ ] Title tag uses local search terms
- [ ] Meta description is natural in target language
- [ ] Body content uses local synonyms and phrasing
- [ ] URL slug is in target language (not English)

## 4. Local Entity References

Check for locale-relevant entities that build trust:

- [ ] Local brands/companies mentioned (not just US/global ones)
- [ ] Local regulations/standards referenced where relevant
- [ ] Local data/statistics used (not just US data)
- [ ] Local experts or authorities cited
- [ ] Geographic references match target market

## 5. Content Parity Analysis

Compare the localized page against the source page for completeness.

### Parity Checklist

| Element | Source | Localized | Match? |
|---------|--------|-----------|--------|
| Word count | [n] | [n] | Within ±20%? |
| Headings (H2-H6) | [n] | [n] | Same structure? |
| Images | [n] | [n] | All present? |
| Internal links | [n] | [n] | Equivalent links? |
| CTAs | [n] | [n] | All translated? |
| Schema markup | [types] | [types] | Same types? |
| Structured data language | en | [locale] | Correct? |

**Important**: Localized content doesn't need to be identical. Some sections may be expanded or condensed for cultural relevance. Focus on equivalent value, not word-for-word match.

## 6. Regional Content Gaps

Identify content that exists in one locale but not others:

```
## Regional Content Gap Report

### Pages Missing Localization
| Source URL | Locale | Priority | Reason |
|-----------|--------|----------|--------|
| /blog/guide | de | High | Gets 500+ DE organic visits to EN version |
| /pricing | ja | Critical | Revenue page, JP is target market |

### Locale-Specific Content Needed
| Locale | Topic | Reason |
|--------|-------|--------|
| DE | GDPR compliance guide | Legal requirement for DE market |
| JP | Local payment setup | Line Pay, PayPay integration docs |
```

## Output Format

```
## Content Localization Report

**Source URL**: [source url]
**Localized URL**: [localized url]
**Source Locale**: [en-US]
**Target Locale**: [de-DE]

### Translation Quality: [score] / 100
- Red flags: [list or "none"]
- Language consistency: [rating]
- Natural phrasing: [rating]

### Cultural Adaptation: [score] / 100
- Images: [appropriate / needs review]
- Examples: [localized / generic]
- Formats (date, currency, units): [correct / issues found]

### Keyword Localization: [score] / 100
- H1 keyword: "[keyword]" — [correct / needs localization]
- Title tag: [correct / needs localization]
- URL slug: [localized / English]

### Content Parity: [score] / 100
- Word count: source [n] vs localized [n] ([x]% delta)
- Missing sections: [list]
- Schema markup: [matches / missing types]

### Recommendations
1. [prioritized actions]
```

## Integration

- Hreflang technical validation → `/seo hreflang`
- Missing pages for locale → `/seo content-brief` in target language
- Keyword research per locale → `/seo keywords research` with location_code
- Mobile parity per locale → `/seo mobile-parity`

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
