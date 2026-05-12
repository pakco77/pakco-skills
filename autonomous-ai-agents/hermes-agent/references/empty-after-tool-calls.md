# Empty assistant response after tool calls

## Symptom

Typical CLI/status signals:
- Hermes shows: `⚠️ Model returned empty after tool calls — nudging to continue`
- The session transcript gains an injected user nudge:
  `You just executed tool calls but returned an empty response. Please process the tool results above and continue with the task.`
- The session JSON shows valid tool results, but the following assistant turn has `"content": "(empty)"` or an empty string.

## Important distinction

Do **not** confuse these cases:

1. **Normal**: assistant message has empty/blank `content` **and** carries structured `tool_calls`.
   - This is expected for many tool-using models.
2. **Problematic**: after tool results are appended, the next assistant turn has **neither** visible text **nor** new `tool_calls`.
   - This is the case that triggers Hermes' empty-after-tool recovery.

## What Hermes is doing

Hermes has an explicit recovery path in `run_agent.py`:
- `13684-13718` — detects an empty post-tool assistant response, appends `(empty)`, then injects a user nudge asking the model to continue.
- `13755-13817` — retries empty responses and then falls back to the configured fallback chain before finally returning `(empty)`.

Interpretation: tools usually **did run successfully**. The failure is often on the provider/model side when generating the **post-tool follow-up assistant text**.

## Common triggers

This class of issue is more likely when:
- switching model/provider mid-session
- continuing a long, tool-heavy conversation
- using an OpenAI-compatible custom endpoint with imperfect tool-follow-up behavior
- mixing one provider for the main chat and another for auxiliary tasks during a resumed session

Observed example from a real session:
- session id: `20260510_230403_b61b40`
- custom provider via `https://www.zeoapi.com/v1`
- model: `gpt-5.4-xhigh`
- failure happened after tool results were present, while Hermes' logs did **not** show a hard transport/JSON parse failure

Treat this as a **provider-compatibility class issue**, not as a claim that one specific model is always broken.

## How to verify

1. Inspect the session transcript JSON in `~/.hermes/sessions/`.
   - Confirm tool results exist.
   - Confirm the next assistant message is empty or `(empty)`.
2. Check `~/.hermes/logs/agent.log` for the recovery message.
3. Distinguish it from HTTP/SDK failures.
   - If there is no network/protocol error, the request may have succeeded but returned no visible assistant text.

## Mitigation

Operational mitigations:
- after switching providers/models, start a fresh session (`/new` or relaunch) before continuing a tool-heavy task
- prefer a known-stable provider/model for long tool chains
- configure a fallback chain so Hermes can switch away from the empty-returning backend
- if the issue occurs in a long session, retry in a fresh session with the same task summary instead of blindly continuing the degraded context

## What to capture in a bug report

Capture all of the following:
- session id
- provider
- model
- base_url
- whether the assistant turn had `tool_calls` or was truly empty
- last successful tool name(s)
- relevant `agent.log` lines around the recovery message
- whether the model/provider was switched mid-session

## Why this reference exists

Future troubleshooting should avoid the wrong conclusion:
- **Wrong:** “the tool failed”
- **Usually more accurate:** “the tool succeeded, but the provider/model failed to produce the visible post-tool assistant continuation”
