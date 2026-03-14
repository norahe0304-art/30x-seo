---
name: 30x-seo-local
description: >
  Local SEO audit and optimization for Google Business Profile, Google Maps,
  and Gemini Ask Maps. Covers GBP completeness, NAP consistency, review strategy,
  local schema, GeoGrid visibility, and AI-powered Maps optimization.
  Use when user says "local SEO", "Google Business Profile", "GBP", "Google Maps",
  "Ask Maps", "local pack", "NAP audit", "local citations", "review strategy".
allowed-tools:
  - WebFetch
  - Bash
  - Read
---

# Local SEO Audit & Optimization

## What This Skill Does

Audit and optimize a business's **local search presence** across Google Business Profile, Google Maps, Local Pack, and Gemini Ask Maps.

**Does NOT do**:
- Traditional on-page SEO → use `seo-page`
- Backlink analysis → use `seo-backlinks`
- AI platform visibility (ChatGPT/Claude/Perplexity) → use `seo-ai-visibility`

---

## Process

### Step 1: Gather Business Info

Ask user for:

| Field | Required | Example |
|-------|----------|---------|
| Business name | ✅ | "Blue Bottle Coffee" |
| Website URL | ✅ | "https://bluebottlecoffee.com" |
| Business category | ✅ | "Coffee shop" |
| Service area / city | ✅ | "San Francisco, CA" |
| GBP URL (if known) | Optional | Google Maps link |
| Target keywords | Optional | "specialty coffee SF" |

---

### Step 2: GBP Completeness Audit

Check every GBP field for completeness and optimization:

| Field | Weight | Check |
|-------|--------|-------|
| Business name | Critical | Matches real name, no keyword stuffing |
| Category (primary) | Critical | Most specific category available |
| Categories (secondary) | High | 2-5 relevant additional categories |
| Address | Critical | Accurate, matches website & citations |
| Phone | Critical | Local number, matches website |
| Website URL | Critical | Correct, uses tracking parameters |
| Hours | High | Complete, including special hours |
| Description | High | 750 chars, natural language, intent-rich |
| Attributes | High | All relevant (WiFi, parking, outdoor, etc.) |
| Products/Services | High | Complete list with descriptions |
| Photos | High | 15+ quality photos, refreshed quarterly |
| Q&A | Medium | 10-15 pre-populated entries |
| Posts | Medium | Weekly cadence |

**Scoring**:
```
GBP Score = filled fields / total applicable fields × 100

90-100%: Excellent
70-89%:  Good, quick wins available
50-69%:  Needs work
<50%:    Critical — significant visibility loss
```

---

### Step 3: NAP Consistency Check

**NAP = Name, Address, Phone** — must be identical everywhere.

Check consistency across:

| Platform | Priority |
|----------|----------|
| Google Business Profile | Critical |
| Website (footer, contact page) | Critical |
| Apple Maps / Apple Business Connect | High |
| Bing Places | High |
| Yelp | High |
| Facebook | High |
| Industry directories | Medium |
| Local chambers / associations | Medium |

**Common Issues**:
```
❌ "123 Main St" vs "123 Main Street" vs "123 Main St."
❌ "(415) 555-1234" vs "415-555-1234" vs "+1 415 555 1234"
❌ "Joe's Coffee" vs "Joe's Coffee Shop" vs "Joe's Coffee LLC"
```

**Fix**: Standardize to one canonical format, update everywhere.

---

### Step 4: Local Schema Audit

Check website for LocalBusiness schema markup:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/photo.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94105",
    "addressCountry": "US"
  },
  "telephone": "+1-415-555-1234",
  "url": "https://example.com",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:00",
      "closes": "19:00"
    }
  ],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "230"
  }
}
```

| Check | Status |
|-------|--------|
| LocalBusiness or subtype present | ✅/❌ |
| NAP matches GBP exactly | ✅/❌ |
| GeoCoordinates present | ✅/❌ |
| OpeningHours present | ✅/❌ |
| AggregateRating present | ✅/❌ |
| Multiple locations handled | ✅/❌/N/A |

---

### Step 5: Review Analysis & Strategy

#### Current State Assessment

| Metric | Benchmark |
|--------|-----------|
| Total reviews | Category average in area |
| Average rating | ≥4.2 stars |
| Review velocity | ≥4 new reviews/month |
| Owner response rate | 100% target |
| Response time | <24 hours |
| Review recency | Most recent <7 days |

#### Sentiment Mining

Extract recurring themes from reviews:
- Positive attributes (what customers praise)
- Negative patterns (what needs fixing)
- Keywords customers use naturally → feed back into GBP description

#### Review Strategy Output

```markdown
## Review Velocity Program

### Collection Touchpoints
1. Post-purchase email (2 hours after)
2. SMS follow-up (24 hours after)
3. Receipt QR code → direct review link
4. Staff verbal ask at checkout

### Response Templates
- Positive (5-star): Thank + reference specific detail + invite back
- Mixed (3-4 star): Thank + acknowledge issue + describe fix + invite back
- Negative (1-2 star): Apologize + take offline + describe resolution

### Target Metrics
- Monthly new reviews: [X] (current: [Y])
- Response rate: 100%
- Response time: <24 hours
```

---

### Step 6: Gemini Ask Maps Optimization

This is the **2026 update** — Google Maps now uses Gemini AI for conversational search ("Ask Maps"). The ranking model shifted from keyword matching to intent understanding.

#### What Changed

| Old Model | New Model (March 2026) |
|-----------|----------------------|
| "coffee near me" | "my phone is dying, where can I charge without waiting in line?" |
| Keyword relevance | Intent + attribute matching |
| Static profile data | Real-time activity signals |
| Proximity dominates | Proximity qualifies, engagement ranks |

#### Ask Maps Optimization Checklist

**Attribute Completeness** (Gemini matches user intent to business attributes):
- [ ] All physical attributes (parking, WiFi, outdoor seating, wheelchair access)
- [ ] All service attributes (dine-in, takeout, delivery, reservations)
- [ ] All audience attributes (good for kids, pet-friendly, LGBTQ+ friendly)
- [ ] Payment methods
- [ ] Sustainability practices

**Q&A as AI Training Data**:
- [ ] 10-15 pre-populated Q&As
- [ ] Cover situational queries ("Do you have charging stations?", "Is there a quiet area to work?")
- [ ] Use natural conversational language, not keyword stuffing

**Google Posts Freshness Signal**:
- [ ] Weekly post cadence (offers, events, updates, photos)
- [ ] Posts include relevant attributes and situational context
- [ ] Seasonal/event-based posts for temporal queries

**Photo Strategy for Immersive Navigation**:
- [ ] Storefront photo showing relationship to nearby landmarks
- [ ] Interior photos showing ambiance, seating, facilities
- [ ] Product/menu photos with quality lighting
- [ ] Refresh every quarter with new content
- [ ] Geotagged images

**Review Content as AI Context**:
When customers mention specific attributes in reviews ("great WiFi", "quiet workspace", "fast service"), Gemini uses this as input for matching intent queries.

Strategy:
- Encourage attribute-specific feedback in review requests
- Highlight specific experience details in response templates
- DO NOT solicit fake reviews or keyword-stuffed reviews

---

### Step 7: Local Content Strategy

Website content that supports local search:

| Content Type | Purpose | Priority |
|-------------|---------|----------|
| Location pages | One per physical location | Critical |
| Service area pages | One per service area | High |
| Local FAQ page | Conversational queries | High |
| Local blog posts | Topical authority | Medium |
| Event/news posts | Freshness signals | Medium |

**Location Page Template**:
- H1: [Service] in [City] — [Business Name]
- Unique description (300+ words, not duplicated across locations)
- Embedded Google Map
- LocalBusiness schema
- NAP in structured format
- Service list
- Customer testimonials from that area
- Driving directions from landmarks
- Parking information

---

## Output

### Local SEO Report

```markdown
# Local SEO Audit: [Business Name]
Generated: [Date]

## Overall Score: XX/100

## GBP Completeness: XX/100  ████████░░
- [List of missing/incomplete fields]

## NAP Consistency: XX/100  ██████████
- [Inconsistencies found]

## Reviews: XX/100  ███████░░░
- Rating: X.X ⭐ (X reviews)
- Velocity: X/month
- Response rate: X%
- Key themes: [positive], [negative]

## Local Schema: XX/100  █████░░░░░
- [Missing markup elements]

## Ask Maps Readiness: XX/100  ████████░░
- Attributes: X/Y filled
- Q&A: X entries
- Posts: [frequency]
- Photo freshness: [last updated]

## Priority Actions
1. 🔴 [Critical action]
2. 🟠 [High priority]
3. 🟡 [Medium priority]
4. 🟢 [Quick win]
```

### Deliverables

| Output | Format |
|--------|--------|
| GBP optimization checklist | Markdown checklist |
| NAP corrections | Table of changes needed |
| LocalBusiness schema | Ready-to-use JSON-LD |
| Review strategy | Action plan with templates |
| Ask Maps optimization plan | Prioritized checklist |
| Location page template | HTML/content structure |

---

## Integration with Other Skills

| Related Skill | When to Use Together |
|---------------|---------------------|
| seo-schema | Deep schema validation beyond LocalBusiness |
| seo-content-audit | Audit location page content quality |
| seo-keywords | Local keyword research and search volume |
| seo-serp | Track Local Pack rankings |
| seo-ai-visibility | Monitor AI platform citations |
| seo-technical | Technical SEO for location pages |
| seo-competitor-pages | Analyze competitor local pages |

---

## Monitoring Cadence

| Check | Frequency |
|-------|-----------|
| GBP completeness | Monthly |
| Review metrics | Weekly |
| NAP consistency | Quarterly |
| Ask Maps self-test | Bi-weekly |
| Local Pack position | Weekly |
| Schema validation | After page changes |

---

## Ask Maps Self-Test Queries

Test your business visibility by searching these patterns in Google Maps:

```
"[category] near [landmark]"
"[category] with [attribute] in [city]"
"where can I [intent] near [area]"
"best [category] for [situation] in [city]"
"[category] open now with [specific need]"
```

Document what Gemini says. If your business is missing or described inaccurately, trace the gap back to a specific GBP field, review pattern, or website content issue.

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
