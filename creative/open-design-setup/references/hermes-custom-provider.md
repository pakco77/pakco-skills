# Why HERMES_INFERENCE_PROVIDER doesn't work in ACP mode

Full code trace showing why env vars are bypassed.

## The call chain

```
OD spawns hermes acp --accept-hooks  (with HERMES_INFERENCE_PROVIDER=zeoapi in env)
  → acp_adapter/server.py: new_session()
    → session_manager.create_session()
      → session.py: _make_agent(session_id, cwd)
```

## The key code

**`acp_adapter/session.py:607-608`**:
```python
try:
    runtime = resolve_runtime_provider(requested=requested_provider or config_provider)
```

- `requested_provider` is `None` for new sessions (OD doesn't pass provider in `session/new`)
- `config_provider` = `model_cfg.get("provider")` → reads from `config.yaml` (e.g., `"deepseek"`)

**`hermes_cli/runtime_provider.py:299-315`** — `resolve_requested_provider()`:
```python
def resolve_requested_provider(requested=None):
    if requested and requested.strip():
        return requested.strip().lower()      # ← HIT: "deepseek" from config
    # ... env var check is NEVER REACHED
    env_provider = os.getenv("HERMES_INFERENCE_PROVIDER", "")
    if env_provider:
        return env_provider                   # ← DEAD PATH for ACP
```

The explicit `requested` argument (from config) takes priority over the env var. `HERMES_INFERENCE_PROVIDER` is only consulted when `requested` is None/empty — which never happens in ACP because config always has a provider set.

## The set_model trap

When the user selects a model like `custom:gpt-5.4-xhigh` in OD:

```
OD → session/set_model { modelId: "custom:gpt-5.4-xhigh" }
  → server.py: set_session_model()
    → _resolve_model_selection("custom:gpt-5.4-xhigh", "custom")
      → parse_model_input → provider="custom", model="gpt-5.4-xhigh"
    → _make_agent(requested_provider="custom")
      → resolve_runtime_provider(requested="custom")
        → "custom" (bare) doesn't resolve to zeoapi's base_url → 503
```

**Always select "Default (CLI config)"** to avoid this path.
