---
name: 30x-seo-semantic-search
description: >
  Entity extraction and Knowledge Graph optimization for semantic search.
  Analyzes entity coverage, topic authority signals, entity relationships,
  and Knowledge Panel eligibility. Use when user says "semantic search",
  "entity SEO", "Knowledge Graph", "Knowledge Panel", "entity optimization",
  "topical authority", or "entity extraction".
allowed-tools:
  - WebFetch
  - Read
maturity: experimental
---

# Semantic Search & Entity Optimization

Optimize content for Google's entity-based understanding. Google's Knowledge Graph powers rich results, entity cards, and contextual search features.

## Analysis Method

Fetch the page via WebFetch and analyze entity signals.

## 1. Entity Extraction

Identify entities mentioned on the page and assess their markup:

### Entity Types to Detect

| Entity Type | HTML/Schema Signals | Example |
|-------------|-------------------|---------|
| Organization | JSON-LD Organization, `<meta>` og:site_name | "Acme Corp" |
| Person | JSON-LD Person, author bio, byline | "Jane Smith, CTO" |
| Product | JSON-LD Product, product specs | "Widget Pro 3000" |
| Place | JSON-LD LocalBusiness, address markup | "San Francisco, CA" |
| Event | JSON-LD Event, date/time markup | "TechConf 2026" |
| Topic/Concept | H1/H2 headings, keyword density | "machine learning" |

### Entity Markup Checklist

For each entity found:
- [ ] Has structured data (JSON-LD preferred)
- [ ] Has consistent naming across page (same entity, same text)
- [ ] Links to authoritative source (Wikipedia, official site)
- [ ] `sameAs` property points to disambiguation URLs
- [ ] Entity is contextually connected to page topic

## 2. Topical Authority Assessment

Evaluate how well a site demonstrates authority on a topic cluster.

### Authority Signals

| Signal | Weight | How to Check |
|--------|--------|-------------|
| Content depth | 25% | Word count, subheading coverage, unique insights |
| Internal linking | 20% | Hub-and-spoke structure, pillar → cluster links |
| Entity consistency | 20% | Same entities referenced across related pages |
| External citations | 15% | Links from authoritative sources on same topic |
| Content freshness | 10% | Recent updates, current year references |
| Author expertise | 10% | Author bio with relevant credentials |

### Topical Authority Score

| Score | Rating | Meaning |
|-------|--------|---------|
| 80-100 | Strong authority | Likely to rank for competitive topic queries |
| 60-79 | Building authority | Good foundation, needs more depth |
| 40-59 | Emerging | Missing key content pieces |
| 0-39 | Weak | Insufficient topical coverage |

## 3. Knowledge Panel Eligibility

Assess whether an entity qualifies for a Google Knowledge Panel.

### Requirements

| Requirement | Status | Check |
|-------------|--------|-------|
| Wikipedia/Wikidata entry | Critical | Search Wikidata for entity |
| Consistent NAP across web | High | Name, Address, Phone match across sites |
| Official website claimed | High | Google Business Profile, social profiles |
| Structured data on site | Medium | Organization/Person JSON-LD |
| `sameAs` links | Medium | Links to Wikipedia, Wikidata, social profiles |
| Notability signals | High | Press coverage, citations, awards |

### Knowledge Panel Readiness Score

- **Ready** (80-100): All critical requirements met, entity has web presence
- **Almost** (60-79): Most requirements met, minor gaps
- **Not ready** (0-59): Major requirements missing

## 4. Entity Relationship Mapping

Map how entities on the page connect to each other and to the broader topic.

### Relationship Types

```
[Organization] --employs--> [Person]
[Person] --authored--> [Article]
[Article] --about--> [Topic]
[Product] --madeBy--> [Organization]
[Event] --hostedBy--> [Organization]
[Place] --locatedIn--> [Region]
```

### What to Look For

- **Orphan entities**: Mentioned but not connected to other entities
- **Missing relationships**: Obvious connections not marked up
- **Disambiguation needs**: Generic terms that could mean multiple things

## 5. Semantic Content Gap Analysis

Identify entities and subtopics that should be present but are missing.

### Method

1. Identify the page's primary topic from H1 + meta description
2. Determine expected entities for that topic (based on top-ranking content)
3. Flag missing entities that competitors cover

### Gap Report Format

```
## Semantic Content Gaps

**Topic**: [primary topic]

### Expected Entities Not Found
| Entity | Type | Why It Matters |
|--------|------|---------------|
| [entity] | Person | Key authority figure in this field |
| [entity] | Concept | Core subtopic competitors all cover |

### Recommended Additions
1. Add section about [missing subtopic] with [entity] references
2. Include [person] quote or citation for authority signal
3. Link to [entity] Wikipedia page for disambiguation
```

## Output Format

```
## Semantic Search Report

**URL**: [url]
**Primary Topic**: [detected topic]
**Entity Score**: [0-100] / 100

### Entities Detected
| Entity | Type | Has Schema | Has sameAs | Authority Link |
|--------|------|-----------|-----------|---------------|
| [name] | Organization | ✅ | ✅ | ✅ |
| [name] | Person | ❌ | ❌ | ✅ |

### Topical Authority
- Authority score: [x] / 100
- Content depth: [rating]
- Internal linking: [rating]
- Entity consistency: [rating]

### Knowledge Panel Readiness
- Entity: [name]
- Readiness: [Ready / Almost / Not ready]
- Missing: [list]

### Recommendations
1. [prioritized actions]
```

## Integration

- Entity gaps found → `/seo content-brief` to plan content covering missing entities
- Weak authority → `/seo internal-links` to build hub-and-spoke structure
- Missing schema → `/seo schema` to generate entity markup

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
