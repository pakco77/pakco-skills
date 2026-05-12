---
name: open-design-setup
description: Set up and run Open Design (nexu-io/open-design) — the open-source Claude Design alternative with 113 design skills, 72+ design systems, and native Hermes support. Covers clone, install, start, stop, and Hermes skill integration.
---

# Open Design Setup

## What it is

Open Design (OD) is an open-source alternative to Claude Design. Local-first, web-deployable, BYOK. Auto-detects 16 coding-agent CLIs on your PATH (including Hermes). Ships 113 design skills and 72+ brand design systems. Runs as a daemon + web UI + optional Electron desktop.

Repo: https://github.com/nexu-io/open-design

## Quick Install & Run

```bash
# Clone (needs longer timeout — repo is large)
git clone --depth 1 https://github.com/nexu-io/open-design.git /tmp/open-design

cd /tmp/open-design
pnpm install
pnpm tools-dev
```

## Packaged App vs Tools-Dev

Open Design has two distinct runtimes — they share nothing except the design-skills directory:

| | Packaged App | Tools-Dev |
|---|---|---|
| **Binary** | `/Applications/Open Design.app` | `pnpm tools-dev` from `/tmp/open-design` |
| **Namespace** | `release-stable` | `default` |
| **Daemon port** | Dynamic (check `lsof -i -P -n \| grep daemon`) | Dynamic (printed at start) |
| **Agents.ts** | Bundled inside .app (not directly editable) | `/tmp/open-design/apps/daemon/src/agents.ts` |
| **Data dir** | `~/Library/Application Support/Open Design/namespaces/release-stable/` | `/tmp/open-design/.tmp/tools-dev/default/` |
| **IPC socket** | `/tmp/open-design/ipc/release-stable/daemon.sock` | `/tmp/open-design/ipc/default/daemon.sock` |

**How to tell which one the user is on:** run `ps aux | grep 'hermes acp\|daemon' | grep -v grep`. If you see `/Applications/Open Design.app/` — they're on the packaged app. If you see `tsx` + `/tmp/open-design/apps/daemon/src/` — tools-dev.

When debugging, always query the correct daemon port. Both run simultaneously without conflict.

### Agent Detection in Packaged App

The packaged app's system PATH does NOT include venv binaries. If `hermes` is installed in a venv (common), it won't be detected. **Do not** try to symlink `hermes` into `/usr/local/bin` (permission denied under SIP) or `~/.local/bin` (not on GUI app PATH).

**Fix:** use `launchctl setenv HERMES_BIN <absolute-path-to-hermes>`, then quit and reopen the packaged app. The `AGENT_BIN_ENV_KEYS` map in `agents.ts` reads `HERMES_BIN` from the process environment.

```bash
launchctl setenv HERMES_BIN /Users/<user>/hermes-agent/venv/bin/hermes
# Verify:
launchctl getenv HERMES_BIN
```

### ZeoAPI / Custom Provider with OD

When using a custom provider (like ZeoAPI) through OD + Hermes ACP:

1. **`HERMES_INFERENCE_PROVIDER` env var is IGNORED in ACP mode.** The ACP `_create_agent` function reads `config.yaml`'s `model.provider` with higher priority than the env var. Only way to switch provider is to change `config.yaml`.

2. **Model speed matters.** OD's ACP stage timeout is 180 seconds (`DEFAULT_STAGE_TIMEOUT_MS`). Reasoning-heavy models (e.g. `gpt-5.4-xhigh` with long thinking phases) can easily exceed this on complex design prompts. Use faster models (`gpt-5.4`, `gpt-5.4-medium`).

3. **ACP model listing prefix.** Custom providers show as `custom:<model>` in OD's model picker, not the config provider name. This is cosmetic — the actual inference uses the correct base_url from config.

## Pitfalls

### 1. Clone timeout
`git clone` with `--depth 1` may need up to 120s timeout. Don't set 30s or less.

### 2. pnpm not installed
```bash
# macOS: corepack enable needs sudo
sudo corepack enable
sudo corepack prepare pnpm@10.33.2 --activate
```
Requires Node ~24 (v24.14.1 confirmed working).

### 3. pnpm approve-builds is interactive
After `pnpm install`, if warned about ignored build scripts (sharp, electron-winstaller), the `pnpm approve-builds` command opens an interactive selector that doesn't work well in Hermes terminal. Workaround: start `pnpm tools-dev` directly — it works without approving.

### 4. pnpm tools-dev exits after starting
`pnpm tools-dev start` launches daemon + web + desktop as background processes and exits. This is normal. Check with `pnpm tools-dev status` or curl the web port.

### 5. Ports are dynamic
Ports change each run. Check startup output for actual URLs.

## Lifecycle Commands

```bash
cd /tmp/open-design

pnpm tools-dev           # start (default)
pnpm tools-dev start     # explicit start
pnpm tools-dev stop      # stop all
pnpm tools-dev status    # check what's running
pnpm tools-dev logs      # view logs
```

Services: daemon (API), web (Next.js UI), desktop (Electron, optional).

## Hermes Skill Integration

All 113 Open Design skills can be installed into Hermes in one shot:

```bash
mkdir -p ~/.hermes/skills/open-design
cp -r /tmp/open-design/skills/* ~/.hermes/skills/open-design/
```

Skills will appear under category "open-design" in Hermes's skill list. Each SKILL.md includes frontmatter with `name`, `description`, `triggers`, and `od` config. The `od` fields (mode, platform, design_system, etc.) are Open Design app-specific and ignored by Hermes — the core workflow instructions in the markdown body remain useful standalone.

## Architecture Note

Open Design uses the daemon to spawn your local coding-agent CLI (Hermes included) with real Read/Write/Bash/WebFetch tools. The web UI provides a structured design flow: pick skill → fill discovery form → pick visual direction → agent generates HTML artifacts → sandboxed preview.
The `DESIGN.md` files in `design-systems/` are injected as system prompts when an agent runs through the OD daemon. When using OD skills directly in Hermes without the daemon, you lose this design-system injection — the skill instructions will tell the agent to "read the active DESIGN.md" which won't exist. Consider providing design direction explicitly in your prompt.

## Configuring a Different Provider/Model for OD + Hermes

OD delegates provider/model to the CLI agent. For Hermes, `hermes acp` has **no `--model` flag** — the adapter can't pass a model choice at spawn time. And critically, **`HERMES_INFERENCE_PROVIDER`/`HERMES_INFERENCE_MODEL` env vars are NOT read by ACP sessions** (see `references/hermes-custom-provider.md` for the full code trace).

### ✅ CORRECT approach: Change Hermes's default provider in config.yaml

The ACP `_create_agent()` method (`acp_adapter/session.py:608`) reads `config.provider` directly from `config.yaml`, NOT from env vars. The only reliable way to switch the provider is to change the config:

```yaml
# ~/.hermes/config.yaml
model:
  default: gpt-5.4-xhigh        # model for this provider
  provider: zeoapi               # MUST match a key in providers: section
  base_url: https://www.zeoapi.com/v1
providers:
  zeoapi:
    base_url: https://www.zeoapi.com/v1
    api_key_env: ZEO_API_KEY
    api_mode: chat_completions
credential_pool_strategies:
  zeoapi: fill_first             # required for custom providers
```

Then restart OD so it re-detects Hermes:
```bash
cd /tmp/open-design
pnpm tools-dev stop
pnpm tools-dev start
```

**⚠️ This changes Hermes's default for ALL usage, not just OD.** If you need a different default for CLI use, you'll need to pass `--provider` / `--model` flags or `HERMES_INFERENCE_*` env vars when using Hermes directly.

### ❌ Approaches that DON'T work

| Approach | Why it fails |
|----------|-------------|
| `env: { HERMES_INFERENCE_PROVIDER: ... }` in OD adapter | ACP `_create_agent()` reads `config.provider` directly (bypasses env) |
| `env: { HERMES_INFERENCE_MODEL: ... }` in OD adapter | Same — `config.default` takes priority |
| Passing `--model` in adapter `buildArgs` | `hermes acp` has no `--model` flag |
| Adding models to OD `fallbackModels` | Only used when ACP detection fails; live model list always wins |

### After config change: what to expect in OD UI

- The Hermes model list will show e.g. `custom:gpt-5.4-xhigh` — the `custom:` prefix is Hermes's internal type for user-defined providers (as opposed to built-in like `deepseek:`)
- Select **"Default (CLI config)"** — this skips `set_session_model` and uses the config directly
- Avoid selecting the explicit `custom:gpt-5.4-xhigh` entry — it triggers `set_session_model` which parses `custom:` as a bare custom provider (without base_url) and may fail with 503

### Rebuilding after adapter changes

If you DO modify `agents.ts` (e.g., adding models to fallbackModels), you MUST rebuild:
```bash
cd /tmp/open-design
pnpm tools-dev stop
pnpm --filter @open-design/daemon build
pnpm tools-dev start
```

The daemon log at `.tmp/tools-dev/default/logs/daemon/latest.log` only shows startup events. Agent runtime errors go to stderr of the spawned process.
