# OpenCode Compatibility

30x SEO skills and agents are compatible with OpenCode with minimal setup.

## Skills

OpenCode discovers skills from these directories (in priority order):
1. `.opencode/skills/<name>/SKILL.md` (project-local)
2. `.claude/skills/<name>/SKILL.md` (Claude Code compatible)
3. `.agents/skills/<name>/SKILL.md` (agent standard)
4. `~/.config/opencode/skills/<name>/SKILL.md` (global)

**30x SEO already works** because OpenCode supports `~/.claude/skills/` which is where the install script places skills.

## Agents

OpenCode uses a different agent discovery path. To make 30x SEO agents available:

### Option 1: Symlink (recommended)

```bash
# Create OpenCode agent directory
mkdir -p ~/.config/opencode/agents

# Symlink 30x-seo agents
for f in /path/to/30x-seo/agents/*.md; do
  ln -sf "$f" ~/.config/opencode/agents/
done
```

### Option 2: Copy

```bash
cp /path/to/30x-seo/agents/*.md ~/.config/opencode/agents/
```

## Format Compatibility

Both Claude Code and OpenCode use the same YAML frontmatter format:

```yaml
---
name: agent-name
description: What this agent does.
tools: Read, WebFetch, Write
---
```

**Key difference**: OpenCode runs agents as separate subprocesses via extensions, while Claude Code uses integrated subagents. The 30x SEO agent instructions are written to work in both modes.

## Tool Compatibility

| Tool | Claude Code | OpenCode |
|------|------------|----------|
| Read | Yes | Yes |
| Write | Yes | Yes |
| Bash | Yes | Yes |
| WebFetch | Yes | Yes |
| Grep | Yes | Yes |
| Glob | Yes | Yes |

All tools used by 30x SEO agents are available in both platforms.
