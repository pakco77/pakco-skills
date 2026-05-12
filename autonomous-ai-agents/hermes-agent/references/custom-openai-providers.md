# Custom OpenAI-Compatible Providers in Hermes

When you need to use a provider that isn't in Hermes' built-in provider list (OpenAI, Anthropic, DeepSeek, OpenRouter, etc.), configure it as a custom OpenAI-compatible endpoint.

## Configuration Steps

### 1. Add the API key to `.env`

```bash
echo 'MY_PROVIDER_API_KEY=sk-xxx...' >> ~/.hermes/.env
```

### 2. Add the provider in config.yaml

Edit `~/.hermes/config.yaml`:

```yaml
providers:
  myprovider:
    base_url: https://api.myprovider.com/v1
    api_key_env: MY_PROVIDER_API_KEY
```

- `base_url` must point to an OpenAI-compatible chat completions endpoint
- `api_key_env` references the env var name (NOT the key value directly)

### 3. Use it

```bash
hermes chat -m model-name --provider custom:myprovider -q "..."
# Interactive model picker:
hermes model
```

The provider name in `--provider` uses the `custom:` prefix: `custom:myprovider`.

### 4. Credential pool (REQUIRED for key resolution)

Contrary to intuition, **you must add a credential pool strategy** for the custom provider in `config.yaml`. Without it, Hermes may resolve the wrong credential (e.g., fall through to OpenRouter) and return HTTP 401:

```yaml
credential_pool_strategies:
  myprovider: fill_first
```

Add this alongside the `providers` block. The `fill_first` strategy tells Hermes to use the first available credential for that provider, resolved via `api_key_env`.

**PITFALL**: If you skip `credential_pool_strategies`, `hermes chat -v` will log:
```
🔑 Using API key: sk-or-v1...   ← WRONG KEY!
```
even though `.env` has the correct key. The `api_key_env` field in the provider config only works when the credential pool strategy is registered.

## Model Naming

The model names are whatever the upstream API returns in `/v1/models`. Query them:

```bash
curl -s https://api.myprovider.com/v1/models \
  -H "Authorization: Bearer $MY_PROVIDER_API_KEY" \
  | python3 -m json.tool
```

## Known Custom Providers

### ZeoAPI (zeoapi.com)

| Field | Value |
|-------|-------|
| Base URL | `https://www.zeoapi.com/v1` |
| Env var | `ZEO_API_KEY` |
| Provider name | `custom:zeoapi` |
| Config section | `providers.zeoapi` in config.yaml |

**Model naming convention**: `gpt-5.4-xhigh`, `gpt-5.4-high`, `gpt-5.4-medium`, `gpt-5.x` etc.

**Token Groups (⚠️ critical)**: ZeoAPI requires selecting the correct **令牌分组 (Token Group)** when creating the API token in their console. Wrong group → "model not found" error.

| Group | Models | Price |
|-------|--------|-------|
| `codex` | gpt-5.4 series, gpt-5.3-codex | ¥0.05/次 |
| `auto` (default) | All available models | — |
| `claudecode-anti` | claude-sonnet-4-6, claude-opus-4-6 | ¥0.35/次 |

**Pitfall**: If the token was created without selecting a group, it falls back to `auto`. If `auto` doesn't include the model you need, recreate the token with the correct group at `https://www.zeoapi.com/console`.

**Chat completions test**:
```bash
curl -s https://www.zeoapi.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZEO_API_KEY" \
  -d '{"model":"gpt-5.4-xhigh","messages":[{"role":"user","content":"hello"}]}'
```
