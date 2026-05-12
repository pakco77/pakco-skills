# Credential Resolution in Hermes Agent

How Hermes finds API keys — and why a provider may work even when `.env` appears empty.

## Key Sources (Priority Order)

1. **`.env` file** (`~/.hermes/.env`) — environment-specific secrets, loaded at startup
2. **`config.yaml`** — `model.api_key` field (less common)
3. **Credential pool** (`~/.hermes/auth.json`) — managed via `hermes auth add/list/remove`
4. **Environment variables** — e.g. `export DEEPSEEK_API_KEY=xxx` before launching
5. **OpenRouter fallthrough** — if `OPENROUTER_API_KEY` is set and provider resolves through OpenRouter's proxy

## Common Confusion Patterns

| Symptom | Likely Cause |
|---------|-------------|
| `.env` lacks `DEEPSEEK_API_KEY` but DeepSeek works | Credential pool or OpenRouter routing |
| Deleting a key from `.env` doesn't break anything | Another key source still supplies credentials |
| `hermes auth remove deepseek 1` doesn't match `.env` contents | The pool is independent of `.env` |

## Editing `.env`

The `patch` tool **cannot write to `.env`** (protected file). Use terminal:

```bash
# Delete a line
sed -i '' '/DEEPSEEK_API_KEY=7878/d' ~/.hermes/.env

# Add/replace a key
sed -i '' '/DEEPSEEK_API_KEY/d' ~/.hermes/.env
echo 'DEEPSEEK_API_KEY=sk-your-key-here' >> ~/.hermes/.env
```

Or use the official CLI:
```bash
hermes config set model.api_key <key>    # sets in config.yaml (not .env)
hermes auth add                          # interactive credential wizard → auth.json
```

## The `auth.json` File

- Stored at `~/.hermes/auth.json`
- **Protected** — the `read_file` tool and `cat` via terminal are blocked from reading it
- Managed exclusively through `hermes auth` subcommands
- Supports multiple keys per provider (rotation via `credential_pool_strategies`)

## Verification

To check which provider and model are actually in use:

```bash
hermes config get model.provider
hermes config get model.default
hermes config env-path    # print .env path
hermes auth list          # show pooled credentials (without exposing secrets)
```

## Key Takeaway

Don't assume `.env` is the only source of truth. If a provider works without a `.env` entry, check:
1. `hermes auth list` — credential pool
2. Whether OpenRouter is proxying the provider
3. Whether config.yaml has a `model.api_key` set directly
