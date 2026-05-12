# Unified Skill Library Architecture

## Problem

Three agents (Hermes, Claude Code, Codex), three separate skill stores. Adding/updating a skill means writing it three times. The goal: **one Git repo, one format (SKILL.md), all agents consume from the same source.**

## Three-Layer Architecture

```
Layer 3: Agent Adapters
  hermes → native (auto-discover from ~/.hermes/skills/)
  claude → "claude-skills sync" generates ~/.claude/skills.md (aggregate index)
  codex  → "codex-skills sync" generates ~/.codex/instructions.md

Layer 2: Sync & Version
  GitHub: pakco77/pakco-skills
  Multi-machine via git pull/push

Layer 1: Canonical Store
  ~/.hermes/skills/  (IS the Git repo)
  SKILL.md format, organized by category/
```

## Design Decisions

1. **~/.hermes/skills/ IS the Git repo** — not a separate project directory. Hermes auto-discovers skills here; other agents consume via adapters that point to the same path. Single source of truth, no sync lag.

2. **Adapters generate indexes, not copies** — Claude Code and Codex don't copy skill content. They get a generated index file that lists all skills with pointers to `~/.hermes/skills/<category>/<name>/SKILL.md`. The agent reads the full skill on demand. Guarantees zero drift.

3. **SKILL.md is the canonical format** — YAML frontmatter (name, description) + Markdown body. Hermes native format, parsable by any agent.

## Adapter Design

### Claude Code Adapter

- Script: `claude-skills sync`
- Output: `~/.claude/skills.md` (aggregate index)
- Content: table of contents of all skills, each with name + description + `Read` command path
- Insert reference into `~/.claude/CLAUDE.md`: "技能库在 ~/.hermes/skills/，用 Read 工具按需加载具体技能"

### Codex Adapter

- Script: `codex-skills sync`
- Output: `~/.codex/instructions.md`
- Same pattern: index file with pointers, `Read` on demand

## Daily Workflow

```
New skill:
  pakco-skills new my-skill → SKILL.md skeleton → write content
  → pakco-skills sync → all agents updated
  → git commit + push

Update skill:
  edit ~/.hermes/skills/<name>/SKILL.md
  → pakco-skills sync
  → git commit + push

New machine:
  git clone pakco77/pakco-skills ~/.hermes/skills/
  → pakco-skills sync
  → all agents ready
```

## Principle

**Only write skills in one place. Adapters only reference, never copy.**
