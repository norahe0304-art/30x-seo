# Architecture

## Overview

30x SEO follows Anthropic's official Claude Code skill specification with a modular, multi-skill architecture.

## Directory Structure

```
30x-seo/
├── skills/
│   ├── 30x-seo/              # Main orchestrator skill
│   │   ├── SKILL.md          # Entry point with routing logic
│   │   └── references/       # On-demand reference files
│   │       ├── cwv-thresholds.md
│   │       ├── schema-types.md
│   │       ├── eeat-framework.md
│   │       └── quality-gates.md
│   │
│   ├── 30x-seo-page/             # Single page analysis
│   ├── 30x-seo-technical/        # Technical SEO
│   ├── 30x-seo-content-audit/    # E-E-A-T analysis
│   ├── 30x-seo-schema/           # Schema markup
│   ├── 30x-seo-sitemap/          # Sitemap analysis/generation
│   ├── 30x-seo-hreflang/         # Hreflang/i18n SEO
│   ├── 30x-seo-images/           # Image optimization
│   ├── 30x-seo-internal-links/   # Internal link analysis
│   ├── 30x-seo-backlinks/        # Backlink profile (DataForSEO)
│   ├── 30x-seo-redirects/        # Redirect chain analysis
│   ├── 30x-seo-content-brief/    # Content briefs
│   ├── 30x-seo-content-writer/   # Content writing guidelines
│   ├── 30x-seo-content-decay/    # Content decay detection
│   ├── 30x-seo-cannibalization/  # Keyword cannibalization
│   ├── 30x-seo-plan/             # Strategic planning
│   ├── 30x-seo-architecture/     # Site architecture
│   ├── 30x-seo-programmatic/     # Programmatic SEO
│   ├── 30x-seo-competitor-pages/ # Competitor comparison pages
│   ├── 30x-seo-monitor/          # GSC monitoring
│   ├── 30x-seo-serp/             # SERP tracking (DataForSEO)
│   ├── 30x-seo-ai-visibility/    # AI visibility (DataForSEO)
│   ├── 30x-seo-keywords/         # Keyword research (DataForSEO)
│   ├── 30x-seo-geo-technical/    # AI crawler management
│   ├── 30x-seo-fake-freshness/  # Fake freshness detection
│   ├── 30x-seo-mobile-parity/   # Mobile content parity
│   ├── 30x-seo-discover/        # Google Discover optimization
│   ├── 30x-seo-rank-tracking/   # Historical rank tracking
│   ├── 30x-seo-competitive-tracking/ # Competitor monitoring
│   └── 30x-seo-cwv-analytics/   # CrUX CWV deep dive
│
├── agents/
│   ├── seo-technical.md      # Technical SEO specialist
│   ├── seo-content.md        # Content quality reviewer
│   ├── seo-schema.md         # Schema markup expert
│   ├── seo-sitemap.md        # Sitemap architect
│   ├── seo-performance.md    # Performance analyzer
│   └── seo-visual.md         # Visual analyzer
│
├── scripts/                  # Python utilities
├── hooks/                    # Pre/post edit hooks
└── docs/                     # Documentation
```

## Component Types

### Skills

Skills are markdown files with YAML frontmatter that define capabilities and instructions.

**SKILL.md Format:**
```yaml
---
name: skill-name
description: >
  When to use this skill. Include activation keywords
  and concrete use cases.
---

# Skill Title

Instructions and documentation...
```

### Subagents

Subagents are specialized workers that can be delegated tasks. They have their own context and tools.

**Agent Format:**
```yaml
---
name: agent-name
description: What this agent does.
tools: Read, WebFetch, Write, Glob, Grep
---

Instructions for the agent...
```

### Reference Files

Reference files contain static data loaded on-demand to avoid bloating the main skill.

## Orchestration Flow

### Full Audit (`/seo audit`)

```
User Request
    │
    ▼
┌─────────────────┐
│   30x-seo       │  ← Main orchestrator
│   (SKILL.md)    │
└────────┬────────┘
         │
         │  Detects business type
         │  Spawns subagents in parallel
         │
    ┌────┴────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│tech   │ │content│ │schema │ │sitemap│ │perf   │ │visual │
│agent  │ │agent  │ │agent  │ │agent  │ │agent  │ │agent  │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │        │        │        │        │
    └─────────┴────────┴────┬───┴────────┴────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Aggregate    │
                    │  Results      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Generate     │
                    │  Report       │
                    └───────────────┘
```

### Individual Command

```
User Request (e.g., /seo page)
    │
    ▼
┌─────────────────┐
│   30x-seo       │  ← Routes to sub-skill
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   30x-seo-page  │  ← Sub-skill handles directly
│   (SKILL.md)    │
└─────────────────┘
```

## Design Principles

### 1. Progressive Disclosure

- Main SKILL.md is concise (<200 lines)
- Reference files loaded on-demand
- Detailed instructions in sub-skills

### 2. Parallel Processing

- Subagents run concurrently during audits via `run_in_background: true`
- Independent analyses don't block each other
- Results aggregated after all complete
- 5-minute timeout per subagent; partial results accepted on timeout
- Missing sections flagged in final report rather than blocking

### 3. Quality Gates

- Built-in thresholds prevent bad recommendations
- Location page limits (30 warning, 50 hard stop)
- Schema deprecation awareness
- FID → INP replacement enforced

### 4. Industry Awareness

- Templates for different business types
- Automatic detection from homepage signals
- Tailored recommendations per industry

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Skill | `30x-seo-{name}/SKILL.md` | `30x-seo-page/SKILL.md` |
| Agent | `seo-{name}.md` | `seo-technical.md` |
| Reference | `{topic}.md` | `cwv-thresholds.md` |
| Script | `{action}_{target}.py` | `fetch_page.py` |
| Template | `{industry}.md` | `saas.md` |

## Extension Points

### Adding a New Sub-Skill

1. Create `skills/30x-seo-newskill/SKILL.md`
2. Add YAML frontmatter with name and description
3. Write skill instructions
4. Update main `30x-seo/SKILL.md` to route to new skill

### Adding a New Subagent

1. Create `agents/seo-newagent.md`
2. Add YAML frontmatter with name, description, tools
3. Write agent instructions
4. Reference from relevant skills

### Adding a New Reference File

1. Create file in appropriate `references/` directory
2. Reference in skill with load-on-demand instruction
