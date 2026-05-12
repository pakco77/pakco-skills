---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow, **or** a third‑party API provider (see
  "Third‑Party API Provider" below)
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## Third‑Party API Provider Configuration

Codex can be pointed at any OpenAI‑compatible API provider (ZeoAPI, Together,
OpenRouter, etc.) instead of OpenAI's native auth.

### Configuration files

Two files under the user's Codex config directory must be set:

| Platform | Config directory |
|----------|-----------------|
| macOS / Linux | `~/.codex/` |
| Windows      | `%USERPROFILE%\\.codex\\` |

**`config.toml`** — define a custom model provider and set it as default:

```toml
disable_response_storage = true
model = "gpt-5.4"                           # model name from the provider
model_provider = "apicat"                    # arbitrary provider keyname
model_reasoning_effort = "xhigh"
model_verbosity = "high"

[features]
web_search_request = true

[model_providers.apicat]                     # must match model_provider keyname
base_url = "https://www.zeoapi.com/v1"       # provider's OpenAI-compatible endpoint
name = "apicat"
requires_openai_auth = true                  # sends auth.json key as Bearer token
wire_api = "responses"                       # "responses" (new) or "chat_completions" (legacy)
```

Key fields explained:

| Field | Value | Notes |
|-------|-------|-------|
| `model` | e.g. `gpt-5.4`, `gpt-5.4-xhigh` | Model name as returned by provider's `/v1/models` |
| `model_provider` | arbitrary string | Must match the table header in `[model_providers.<name>]` |
| `base_url` | full URL to provider's v1 endpoint | Must end in `/v1` |
| `requires_openai_auth` | `true`/`false` | When `true`, reads `OPENAI_API_KEY` from `auth.json` |
| `wire_api` | `"responses"` or `"chat_completions"` | Codex uses the Responses API by default; set `"chat_completions"` if provider doesn't support Responses |

**`auth.json`** — minimal format, API key only:

```json
{
  "OPENAI_API_KEY": "<your-actual-api-key>"
}
```

No extra fields. The key must be the real key, not a masked/truncated display value.

### Procedure

1. **Exit Codex** entirely (old process caches config).
2. **Backup** existing config files with a timestamp suffix:
   ```bash
   cd ~/.codex
   ts=$(date +%Y%m%d-%H%M%S)
   cp config.toml "config.toml.bak-$ts"
   cp auth.json "auth.json.bak-$ts"
   ```
3. **Write** `config.toml` and `auth.json` with the provider's details.
4. **Verify** the API works before restarting Codex:
   ```bash
   # 1. List models
   curl -s -H "Authorization: Bearer $KEY" "$BASE_URL/models"

   # 2. Test chat completion
   curl -s -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
     -d '{"model":"gpt-5.4","messages":[{"role":"user","content":"Reply with exactly OK"}],"max_tokens":16}' \
     "$BASE_URL/chat/completions"
   ```
   Expect `"OK"` in the response.
5. **Restart** Codex, open a new conversation, test with `只回复 OK`.

### Pitfalls

- **Masked key display**: AI tools may visually mask API keys when reading `auth.json`. Do NOT copy the masked value back into the file — always use the real key the user provided.
- **Provider name consistency**: `model_provider` in the top‑level config and the `[model_providers.<name>]` header must match exactly.
- **Both files required**: writing only `config.toml` or only `auth.json` is insufficient.
- **Restart required**: Codex caches config at startup. A live process won't pick up changes.
- **New conversation**: old sessions may retain prior model/provider state. Create a fresh one.
- **Platform path**: Windows paths differ from macOS/Linux. Use `%USERPROFILE%` on Windows, `~` on macOS/Linux.
- **wire_api mismatch**: If the provider doesn't support the Responses API, change `wire_api` to `"chat_completions"`. Try `"responses"` first; if chat requests fail, switch to `"chat_completions"`.

### Known‑good reference

See `references/zeoapi-config.md` for a concrete, tested configuration against
the ZeoAPI provider — model list, exact file contents, and verification output.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
