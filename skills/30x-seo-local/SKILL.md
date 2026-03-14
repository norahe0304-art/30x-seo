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

### Step 2: GBP Completeness Audit (Google Official 13-Point Playbook)

Based on Google's official GBP Optimization Playbook (March 2026).

| # | Field | Weight | Check |
|---|-------|--------|-------|
| 1 | **Business Information** | Critical | Accurate name (no keyword stuffing), address matches license, local phone |
| 2 | **Business Category** | Critical | Most specific primary category from 4,100+ options. **Wrong category = ranking disaster** (documented case: #1 → #31 from wrong category) |
| 3 | **Business Description** | High | 750 chars, concise overview of offerings + what makes you unique, natural language |
| 4 | **Business Hours** | High | Complete including holidays/special hours. **Longer hours = ranking advantage** (24/7 via answering service outperforms limited hours) |
| 5 | **Service Area** | High | Define geographical service region (service-area businesses) |
| 6 | **Attributes** | High | All relevant (WiFi, parking, outdoor, wheelchair access, etc.) |
| 7 | **Photos & Videos** | High | 15+ quality photos, refresh quarterly. **100+ photos = 520% more calls, 2700% more direction requests** |
| 8 | **Google Posts** | High | Weekly cadence: updates, offers, events. Post 1-2x/week minimum — freshness is a top-tier ranking signal in 2026 |
| 9 | **Social Links** | Medium | Link up to 7 social profiles (5 display). Google may show social posts in profile |
| 10 | **Chat Links** | Medium | Add WhatsApp or SMS Chat for direct customer communication |
| 11 | **Bookings & Orders** | Medium | Enable Reserve with Google, booking links, order buttons. **77% of consumers expect online booking** |
| 12 | **Products/Services** | High | Complete list with descriptions. Add all pre-defined + custom services |
| 13 | **Manage Reviews** | Critical | Actively monitor and respond to every review |

#### Category Selection (Critical)

Primary category is the single most impactful GBP field:
- Choose from Google's 4,100+ options — pick the most specific match
- Monitor category changes regularly (Google updates the list)
- Verify competitors' primary categories for validation
- **Wrong category = catastrophic ranking loss**

#### Attributes to AVOID

These attributes can **hide your reviews** from the profile:
- ❌ "Onsite services" — removes review visibility
- ❌ "Online appointment" — removes review visibility

Only enable these if the booking functionality outweighs review visibility for your business.

#### Reserve with Google

Drive bookings directly from GBP without customers leaving Google:
- Live in 88+ countries
- Covers: beauty, home services, auto repair, fitness, healthcare, restaurants
- Two options: **Custom Booking Link** (your own URL) or **Integrated Booking Partner** (Google partners)
- 77% of consumers expect to book services online — missing this = losing conversions

#### Landing Page Strategy

- Use UTM codes on the GBP website URL to track traffic in GA4
- **Do NOT link to a page that already ranks organically** — Google penalizes duplicate rankings
- Link to a dedicated local landing page optimized for GBP traffic

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

#### The 10-Review Threshold (Sterling Sky Research)

- **10 reviews = minimum threshold** for ranking boost
- After 10, **frequency matters more than total count**
- Stagnant review counts hurt rankings vs. active competitors
- Google formalized review request links and QR codes (late 2025) — use them

#### Current State Assessment

| Metric | Benchmark | Source |
|--------|-----------|--------|
| Total reviews | ≥10 minimum, then category avg | Sterling Sky |
| Average rating | ≥4.2 stars | Industry standard |
| Review velocity | Consistent weekly flow | Sterling Sky |
| Owner response rate | 100% target | Google Playbook |
| Response time | <24 hours | Google Playbook |
| Review recency | Most recent <7 days | Best practice |

#### Sentiment Mining

Extract recurring themes from reviews:
- Positive attributes (what customers praise)
- Negative patterns (what needs fixing)
- Keywords customers use naturally → feed back into GBP description
- Attribute-specific mentions ("great WiFi", "quiet workspace") → these feed Gemini Ask Maps matching

#### Review Strategy Output

```markdown
## Review Velocity Program

### Collection Touchpoints
1. Google's official review request link (GBP dashboard → "Ask for reviews")
2. QR code (Google's built-in generator) on receipts/signage
3. Post-purchase email (2 hours after)
4. SMS follow-up (24 hours after)
5. Staff verbal ask at checkout

### Response Templates
- Positive (5-star): Thank + reference specific detail + invite back
- Mixed (3-4 star): Thank + acknowledge issue + describe fix + invite back
- Negative (1-2 star): Apologize + take offline + describe resolution

### Key Principle
Frequency > quantity. 4 reviews/week beats 50 reviews once then silence.

### Target Metrics
- Weekly new reviews: [X] (current: [Y])
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

### Step 7: AI Local Pack Reality (2026)

Google is rolling out AI-generated local packs that fundamentally change visibility:

| Traditional Local Pack | AI Local Pack (2026) |
|----------------------|---------------------|
| 3 businesses shown | **1-2 businesses shown** |
| Call buttons visible | Call buttons replaced by images |
| Broad business coverage | **Only 32% as many unique businesses** |
| ~1% ad coverage | **22% ad coverage** (up from 1% in early 2025) |

**What this means**:
- Competition for the top 1-2 spots is now existential, not just beneficial
- 68% fewer businesses get organic visibility in AI packs
- Local Services Ads (LSAs) grew from 11% to 31% query coverage
- Pure organic local strategy is no longer sufficient for competitive markets

**Action items**:
- GBP optimization must be flawless (no room for "good enough")
- Consider Local Services Ads for competitive categories
- Multi-location businesses have a structural advantage over single-location
- Diversify traffic sources: YouTube, Reddit, social — don't depend solely on Maps

---

### Step 8: Local Content Strategy

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

## Industry-Specific Guidance

Google released industry-specific GBP Playbooks (March 2026). Apply these vertical optimizations:

### Food & Drink Businesses
- Menu data must be current and complete (add menu URL)
- Enable online ordering + reservation links
- Professional food photography is non-negotiable
- Weekly posts on specials, seasonal menus, events

### Service Businesses (plumbers, cleaners, HVAC, etc.)
- Define service areas clearly (no physical address display if SAB)
- Emphasize emergency availability and response times
- List all certifications, licenses, insurance
- Before/after project photos build visual credibility

### Hotels & Accommodations
- Class ratings and amenity lists
- Room photos, lobby, facilities
- Check-in/check-out times in hours
- Enable Reserve with Google

### Tours & Attractions
- Seasonal hours and availability
- Pricing tiers in products/services
- Activity photos from real customers
- Link to booking system

---

## GBP Pro Tips (Sterling Sky Research)

| Tip | Why |
|-----|-----|
| Set **opening date** to oldest legitimate date | Builds credibility. Use company history, not just current location opening. Google may populate a random date if blank |
| **Extend business hours** when possible | Google favors accessible businesses. 24/7 via answering service = ranking advantage |
| **Do NOT link GBP to a page with existing organic rankings** | Google penalizes duplicate ranking — use a dedicated local page |
| Remove "onsite services" and "online appointment" attributes | They hide review visibility from your profile |
| Add **up to 7 social profiles** | Only 5 display. Google may show social posts. This is a secondary credibility layer for AI engines |

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

---

## Sources (March 2026)

- Google Official GBP Optimization Playbook (emailed March 13, 2026)
- Google Official Industry Playbooks: Food & Drink, Service, Tours & Attractions, Hotels
- Sterling Sky: "The State of Local SEO in 2026"
- Sterling Sky: "#1 Checklist to Optimize Your Google Business Profile"
- Google: Gemini Ask Maps + Immersive Navigation (announced March 12, 2026)

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
