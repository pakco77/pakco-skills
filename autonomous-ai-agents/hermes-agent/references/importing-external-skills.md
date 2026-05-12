# Importing External Skills into Hermes Agent

## Overview

Third-party skill ecosystems package reusable agent behaviors as SKILL.md files.
Hermes can install individual skills from direct URLs, but importing an entire
ecosystem requires checking compatibility. This reference documents the process
with a concrete example.

## General Playbook

### 1. Clone the source repo

```bash
cd /tmp && git clone <repo-url>
```

### 2. Examine the skill format

```bash
ls <repo>/skills/
# Each skill should be a directory with SKILL.md + optional companion files
```

Check that SKILL.md files have YAML frontmatter with `name` + `description`.
This is the minimum Hermes requires. Hermes also supports `version`, `author`,
`license`, `metadata.hermes.{tags, related_skills}` but these are optional for
imported skills.

### 3. Map each skill: built-in overlap?

For each skill in the external ecosystem, check:

- Does Hermes have an equivalent built-in skill? (`skills_list` + `skill_view`)
- Does the external skill add meaningful value beyond what Hermes has?
- Does the external skill reference harness-specific tools or commands that
  don't exist in Hermes (e.g. Claude Code `/commands`, Codex CLI plugins)?

### 4. Check for name collisions

Before importing, check if the skill name already exists as a Hermes built-in or user skill:

```bash
# List all current skills (includes built-in + user-installed)
hermes skills list | grep <skill-name>

# Or check disk for user skills
ls ~/.hermes/skills/ | grep <skill-name>
```

Hermes built-in skills live in the repo's `skills/` directory (not in `~/.hermes/skills/`), so `ls ~/.hermes/skills/` won't detect them. Always use `skills_list` to get the full picture.

### 5a. Single skill with companion files (preferred method)

For individual skills with companion files (scripts, reference prompts, templates):

```bash
# Clone the repo first
cd /tmp && git clone <repo-url>

# Copy the entire skill directory (SKILL.md + all companion files)
cp -r /tmp/<repo>/skills/<skill-name> ~/.hermes/skills/<skill-name>

# Verify the skill loads
hermes skills list | grep <skill-name>
# Also verify via skill_view if available
```

This preserves all scripts, references, and templates alongside the SKILL.md.

### 5b. Single skill SKILL.md only (no companion files)

```bash
# Using hermes skills install from direct URL
hermes skills install https://raw.githubusercontent.com/owner/repo/main/skills/<name>/SKILL.md

# Or if companion files are needed later, still clone + cp
cd /tmp && git clone <repo-url>
cp /tmp/<repo>/skills/<skill-name>/SKILL.md ~/.hermes/skills/<skill-name>/
```

### 5c. Bulk import multiple skills

When importing many skills at once (e.g. an entire ecosystem), use `cp -r` in a loop rather than individual `hermes skills install` calls:

```bash
cd /tmp/<repo>/skills
for name in skill-a skill-b skill-c; do
  if [ -d "$HOME/.hermes/skills/$name" ]; then
    echo "SKIP $name (already exists)"
  else
    cp -r "$name" "$HOME/.hermes/skills/$name"
    echo "INSTALLED $name"
  fi
done
```

Using `cp -r` is the only way to preserve companion files across a bulk import. `hermes skills install` only handles the SKILL.md file and requires one invocation per skill.

### 6. Verify installation

```bash
# Check the skill appears
hermes skills list | grep <skill-name>

# Load and inspect it (if skills_list tool is available)
skill_view(name='<skill-name>')

# Verify linked files are accessible
skill_view(name='<skill-name>', file_path='scripts/start-server.sh')
```

If a skill has linked files (scripts, references) but doesn't show them correctly, the skill directory structure may be incomplete. Re-check the `cp -r` command preserved the directory structure.

### 7. Adapt content (if needed)

### 5. Adapt harness-specific content

If the skill references commands/tools from another platform:
- Replace `/command` references with Hermes equivalents or remove them
- Adapt `<HARD-GATE>` blocks — Hermes injects skill instructions into the
  system prompt, so gating works differently
- Strip Claude Code / Codex-specific tool instructions that won't resolve

---

## Example: obra/superpowers → Hermes

### Ecosystem overview

[obra/superpowers](https://github.com/obra/superpowers) is a development
methodology with ~14 skills. Skills use SKILL.md with YAML frontmatter —
directly compatible with Hermes' skill format.

### Skills already covered by Hermes built-ins (skip these)

| Superpowers Skill | Hermes Equivalent | Notes |
|-|-|-|
| `writing-plans` | `writing-plans` | Same concept, similar detail level |
| `test-driven-development` | `test-driven-development` | Same RED-GREEN-REFACTOR |
| `systematic-debugging` | `systematic-debugging` | Same 4-phase approach |
| `requesting-code-review` | `requesting-code-review` | Pre-commit review workflow |
| `subagent-driven-development` | `subagent-driven-development` | Hermes uses `delegate_task` directly |
| `writing-skills` | `hermes-agent-skill-authoring` | Hermes version adapted to its own tooling |
| `dispatching-parallel-agents` | (covered by `delegate_task` tool) | Not a separate Hermes skill; the tool handles this |

### Skills worth importing (no direct Hermes equivalent)

| Superpowers Skill | What It Does | Import? |
|-|-|-|
| `brainstorming` | Socratic design refinement before coding — asks clarifying questions, presents 2-3 approaches, writes design doc | ✅ Recommended |
| `using-git-worktrees` | Creates isolated git worktree on new branch for each feature | ✅ Recommended (Hermes has `--worktree` flag but no dedicated skill for the workflow) |
| `executing-plans` | Batch execution of plan tasks with human checkpoints | ⚠️ Partially covered by `subagent-driven-development`; Superpowers version is simpler/less autonomous |
| `finishing-a-development-branch` | Verifies tests, presents merge/PR/keep/discard options, cleans up | ⚠️ Partially covered by `github-pr-workflow` |
| `verification-before-completion` | Ensures bug fixes actually work before closing | ✅ Small, focused, no good Hermes equivalent |
| `receiving-code-review` | How to respond to PR review feedback | ✅ Useful if you do collaborative development |

### Potential issues to watch for

1. **HARD-GATE blocks** — Superpowers uses `<HARD-GATE>Do NOT write code until user approves design</HARD-GATE>`. Works fine in Hermes but may interact oddly with Hermes' own tool-use enforcement. Test in a fresh session.

2. **Script references** — Some skills (e.g. `brainstorming`) reference companion files like `spec-document-reviewer-prompt.md` and `visual-companion.md`. These need to be copied alongside the SKILL.md.

3. **Path conventions** — Superpowers saves design docs to `docs/superpowers/specs/`. Hermes saves to `.hermes/plans/`. The skill may need path adjustment or the user needs to know the convention.

4. **Auto-triggering** — Superpowers relies on Claude Code's built-in auto-triggering. Hermes loads skills when explicitly loaded (`/skill name` or `-s name` at startup) or via the system prompt. Imported skills won't auto-trigger in the same way unless loaded explicitly.

### Import command (example)

```bash
# Install brainstorming skill from superpowers
hermes skills install \
  https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/brainstorming/SKILL.md

# Verify
hermes skills list | grep brainstorming
```

For companion files, the user needs to manually copy them:
```bash
mkdir -p ~/.hermes/skills/brainstorming/
cp /tmp/superpowers/skills/brainstorming/*.md ~/.hermes/skills/brainstorming/
```
