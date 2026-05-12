# ZeoAPI — Codex Third-Party Provider (Verified)

Tested configuration for pointing Codex at ZeoAPI
(`https://www.zeoapi.com/v1`) as the model provider.

## Config Files (macOS)

### `~/.codex/config.toml`

```toml
disable_response_storage = true
model = "gpt-5.4"
model_provider = "apicat"
model_reasoning_effort = "xhigh"
model_verbosity = "high"

[features]
web_search_request = true

[model_providers.apicat]
base_url = "https://www.zeoapi.com/v1"
name = "apicat"
requires_openai_auth = true
wire_api = "responses"
```

### `~/.codex/auth.json`

```json
{
  "OPENAI_API_KEY": "<your-zeoapi-key>"
}
```

## Verified Models (via GET /v1/models)

- `gpt-5.3-codex` / `-high` / `-low` / `-medium` / `-xhigh`
- `gpt-5.4` / `-high` / `-low` / `-medium` / `-xhigh`
- `gpt-5.5` / `-high` / `-low` / `-medium` / `-xhigh`

Recommended default: `gpt-5.4`. For stronger reasoning: `gpt-5.4-xhigh`.

## API Verification

### List models
```bash
curl -s -H "Authorization: Bearer $KEY" "https://www.zeoapi.com/v1/models"
```

### Test chat completion
```bash
curl -s -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.4","messages":[{"role":"user","content":"只回复 OK"}],"max_tokens":16}' \
  "https://www.zeoapi.com/v1/chat/completions"
```

### Expected response
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "gpt-5.4",
  "choices": [{"index": 0, "message": {"role": "assistant", "content": "OK"}, "finish_reason": "stop"}],
  "usage": {"prompt_tokens": 9, "completion_tokens": 5, "total_tokens": 14}
}
```

## Notes

- Tested on macOS with `~/.codex/` config directory
- Windows path equivalent: `%USERPROFILE%\\.codex\\`
- `wire_api = "responses"` worked; fall back to `"chat_completions"` if provider doesn't support the Responses API
- Provider keyname `"apicat"` is arbitrary but must be consistent between `model_provider` and `[model_providers.apicat]`
