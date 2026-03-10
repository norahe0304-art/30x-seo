---
name: 30x-seo-blog-pipeline
description: >
  End-to-end SEO blog production pipeline. Takes a seed keyword or topic
  and produces a complete, publish-ready blog post with SEO optimization,
  E-E-A-T signals, schema markup, internal link suggestions, and CMS-ready
  front matter. Supports Hugo, Next.js, WordPress, and generic markdown.
  Use when user says "write blog", "blog pipeline", "generate article",
  "create SEO post", "blog production", "content pipeline", or "auto blog".
allowed-tools:
  - WebFetch
  - Read
  - Bash
  - Grep
  - Glob
maturity: beta
---

# SEO Blog Production Pipeline

End-to-end pipeline: keyword → research → outline → draft → optimize → publish-ready markdown.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo blog-pipeline <keyword>` | Full pipeline: research → outline → draft → optimize |
| `/seo blog-pipeline outline <keyword>` | Research + outline only (no draft) |
| `/seo blog-pipeline draft <outline-file>` | Generate draft from existing outline |
| `/seo blog-pipeline optimize <draft-file>` | SEO-optimize an existing draft |

---

## Pipeline Stages

### Stage 1: Keyword Research & SERP Analysis

**Input**: Seed keyword or topic
**Output**: Target keyword, search intent, SERP landscape

1. **Identify target keyword**
   - If DataForSEO configured: fetch search volume, difficulty, intent
   - Otherwise: analyze keyword from context (length, modifiers, implied intent)

2. **Analyze SERP competition** (via WebFetch)
   - Fetch top 5 ranking pages for the keyword
   - Extract: title patterns, word counts, heading structures, content angles
   - Identify content gaps (what top pages miss)

3. **Determine search intent**
   - Informational: "how to", "what is", "guide"
   - Commercial: "best", "top", "review", "vs"
   - Transactional: "buy", "price", "discount"
   - Navigational: brand + product name

4. **Output**: Research brief

```markdown
## Research Brief
- **Target keyword**: [keyword]
- **Search volume**: [n]/mo (if available)
- **Difficulty**: [score] (if available)
- **Intent**: [informational/commercial/transactional]
- **Top competitors**: [list of top 5 URLs]
- **Avg competitor word count**: [n]
- **Content gaps identified**: [list]
- **Recommended angle**: [unique angle not covered by competitors]
```

---

### Stage 2: Outline Generation

**Input**: Research brief from Stage 1
**Output**: Detailed content outline

1. **Title generation** (3 options)
   - Include target keyword naturally
   - 50-60 characters
   - Compelling for both search and social

2. **Meta description** (2 options)
   - 150-160 characters
   - Include keyword + value proposition
   - Call to action

3. **Heading structure**
   - H1: matches title intent
   - H2s: main sections covering all subtopics from SERP analysis
   - H3s: subsections for depth
   - Logical flow: problem → context → solution → action

4. **Content plan per section**
   - Key points to cover
   - Data/statistics to include
   - Examples or case studies needed
   - Internal link opportunities

5. **Output**: Outline document

```markdown
## Content Outline

### Title Options
1. [Option A — keyword-first]
2. [Option B — benefit-first]
3. [Option C — number/list-based]

### Meta Description Options
1. [Option A]
2. [Option B]

### Structure
- H1: [title]
  - H2: [Introduction / Hook]
    - Hook with statistic or question
    - Brief overview of what reader will learn
  - H2: [Main Topic 1]
    - H3: [Subtopic 1a]
    - H3: [Subtopic 1b]
  - H2: [Main Topic 2]
    - H3: [Subtopic 2a]
  - H2: [Practical Section — How-to / Examples]
  - H2: [FAQ / Common Questions]
  - H2: [Conclusion + CTA]

### Target Specs
- Word count: [n] (based on competitor avg + 20%)
- Images: [n] recommended
- Internal links: [n] target
- External links: [n] to authoritative sources
```

---

### Stage 3: Draft Generation

**Input**: Outline from Stage 2
**Output**: Complete blog post draft

#### Writing Guidelines

**Tone & Style**:
- Write for the target audience (match competitor sophistication level)
- Use active voice, short paragraphs (2-4 sentences)
- Include transition sentences between sections
- Vary sentence length for readability

**SEO Integration** (natural, not forced):
- Target keyword in: H1, first 100 words, 1-2 H2s, meta description, conclusion
- Keyword density: 1-2% (natural usage, never stuffed)
- Semantic variations and LSI keywords throughout
- Long-tail variations in H3s and body

**E-E-A-T Signals**:
- **Experience**: Include first-hand insights, "In our experience...", practical tips
- **Expertise**: Reference specific data, methodologies, technical details
- **Authoritativeness**: Cite authoritative sources (link to studies, official docs)
- **Trustworthiness**: Transparent, balanced view, acknowledge limitations

**AI Citation Readiness** (for AI search visibility):
- Include quotable statistics with sources
- Use clear, definitive statements (not vague)
- Structure facts in easily extractable format
- Optimal passage length: 134-167 words per key point

**Content Quality**:
- Original insights (not just rephrasing competitors)
- Concrete examples, not abstract advice
- Data-backed claims with sources
- Actionable takeaways per section

---

### Stage 4: SEO Optimization Pass

**Input**: Draft from Stage 3
**Output**: Optimized, publish-ready article

#### Optimization Checklist

**On-Page SEO**:
- [ ] Title tag: 50-60 chars, includes keyword, compelling
- [ ] Meta description: 150-160 chars, includes keyword, has CTA
- [ ] H1: exactly one, matches title intent
- [ ] H2-H6: logical hierarchy, no skipped levels
- [ ] Target keyword in first 100 words
- [ ] Keyword density 1-2% (natural)
- [ ] URL slug: short, keyword-included, hyphenated

**Content Quality**:
- [ ] Word count meets or exceeds competitor average
- [ ] Every section has actionable value
- [ ] No filler paragraphs
- [ ] Readability: Flesch-Kincaid grade 8-10

**Links**:
- [ ] 3-5 internal links to related content (suggest based on site structure)
- [ ] 2-4 external links to authoritative sources
- [ ] All links have descriptive anchor text (not "click here")
- [ ] No broken links

**Images**:
- [ ] Suggest image placement (after every 300-400 words)
- [ ] Generate alt text suggestions for each image slot
- [ ] Recommend image types (screenshot, diagram, chart, photo)

**Schema Markup**:
- [ ] Article/BlogPosting JSON-LD generated
- [ ] FAQ schema if FAQ section exists
- [ ] Author schema with credentials

**Technical**:
- [ ] Table of contents suggestion (for 2000+ word posts)
- [ ] Key takeaways / TL;DR box at top (for commercial intent)
- [ ] Related posts suggestions at bottom

---

## Output Format

### File Structure

```
output/
├── [slug].md           # Final article (with front matter)
├── [slug]-outline.md   # Content outline
├── [slug]-schema.json  # JSON-LD schema markup
└── [slug]-meta.md      # SEO metadata summary
```

### Article Front Matter (Hugo)

```yaml
---
title: "[Title]"
date: "[YYYY-MM-DD]"
description: "[Meta description]"
slug: "[url-slug]"
keywords: ["keyword1", "keyword2", "keyword3"]
categories: ["[Category]"]
tags: ["tag1", "tag2"]
author:
  name: "[Author Name]"
  bio: "[Author credentials]"
images: ["[og-image-url]"]
draft: false
schema:
  type: "BlogPosting"
---
```

### Article Front Matter (Next.js / MDX)

```yaml
---
title: "[Title]"
publishedAt: "[YYYY-MM-DD]"
summary: "[Meta description]"
image: "[og-image-path]"
author: "[Author Name]"
tags: ["tag1", "tag2"]
---
```

### Article Front Matter (WordPress)

```yaml
---
title: "[Title]"
excerpt: "[Meta description]"
slug: "[url-slug]"
category: "[Category]"
tags: ["tag1", "tag2"]
featured_image: "[image-url]"
status: "draft"
seo_title: "[SEO Title if different]"
seo_description: "[Meta description]"
---
```

### Article Front Matter (Generic Markdown)

```yaml
---
title: "[Title]"
date: "[YYYY-MM-DD]"
description: "[Meta description]"
keywords: ["keyword1", "keyword2"]
author: "[Author Name]"
---
```

---

## Schema Output

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Title]",
  "description": "[Meta description]",
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "[Author profile URL]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Site Name]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "[Article URL]"
  },
  "wordCount": "[N]",
  "keywords": "[keyword1, keyword2]"
}
```

---

## CMS Detection

When the user's project is available, auto-detect CMS from project files:

| Signal | CMS | Front Matter |
|--------|-----|-------------|
| `hugo.toml` / `config.toml` | Hugo | Hugo format |
| `next.config.js` / `contentlayer.config` | Next.js | MDX format |
| `wp-config.php` / `wordpress` in package.json | WordPress | WP format |
| `.astro/` / `astro.config.mjs` | Astro | Generic + layout |
| `gatsby-config.js` | Gatsby | Generic + frontmatter |
| None detected | Generic | Simple markdown |

Use Glob to check for CMS signals in the project root.

---

## Quality Gates

Before outputting the final article:

| Check | Threshold | Action if Failed |
|-------|-----------|-----------------|
| Word count | ≥ competitor avg | Expand thin sections |
| Keyword in H1 | Required | Rewrite H1 |
| Keyword in first 100 words | Required | Adjust intro |
| Keyword density | 1-2% | Add/remove mentions |
| Internal link suggestions | ≥ 3 | Suggest more |
| External authority links | ≥ 2 | Add sources |
| Heading hierarchy | No gaps | Fix structure |
| Meta description length | 150-160 chars | Trim/expand |
| Readability score | Grade 8-10 | Simplify language |

---

## Integration With Other Skills

| When | Use |
|------|-----|
| Keyword selection | `/seo keywords research` for volume + difficulty data |
| Competitor analysis | `/seo competitive-tracking` for content gaps |
| Content optimization | `/seo content-audit` to validate E-E-A-T score |
| Schema generation | `/seo schema` for advanced structured data |
| Internal linking | `/seo internal-links` for link opportunities |
| Image optimization | `/seo images` for alt text and format guidance |
| Freshness check | `/seo fake-freshness` to ensure genuine updates |
| Discover eligibility | `/seo discover` to optimize for Google Discover |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
