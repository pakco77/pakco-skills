# Codex state_5.sqlite Schema

Location: `~/.codex/state_5.sqlite`

## Table: threads

The main conversation (thread) storage. Each row is one chat session.

```sql
CREATE TABLE threads (
    id TEXT PRIMARY KEY,           -- UUID thread identifier
    rollout_path TEXT NOT NULL,    -- rollout recording path (JSONL)
    created_at INTEGER NOT NULL,   -- unix epoch ms
    updated_at INTEGER NOT NULL,   -- unix epoch ms
    source TEXT NOT NULL,          -- "vscode" or subagent JSON
    model_provider TEXT NOT NULL,  -- "openai", "apicat", etc.
    cwd TEXT NOT NULL,             -- working directory when created
    title TEXT NOT NULL,           -- conversation title
    sandbox_policy TEXT NOT NULL,
    approval_mode TEXT NOT NULL,
    tokens_used INTEGER NOT NULL DEFAULT 0,
    has_user_event INTEGER NOT NULL DEFAULT 0,
    archived INTEGER NOT NULL DEFAULT 0,
    archived_at INTEGER,
    git_sha TEXT,
    git_branch TEXT,
    git_origin_url TEXT,
    cli_version TEXT NOT NULL DEFAULT '',
    first_user_message TEXT NOT NULL DEFAULT '',
    agent_nickname TEXT,
    agent_role TEXT,
    memory_mode TEXT NOT NULL DEFAULT 'enabled',
    model TEXT,                    -- model name (e.g. "gpt-5.4"), NULL = use default
    reasoning_effort TEXT,
    agent_path TEXT,
    created_at_ms INTEGER,
    updated_at_ms INTEGER,
    thread_source TEXT
);
```

## Key columns for provider switching

| Column | Purpose |
|--------|---------|
| `model_provider` | Codex filters conversation list by this value. Mismatch → hidden. |
| `model` | Model name used. Set to NULL when switching providers so Codex picks its default. |
| `archived` | 1 = user archived the thread (separate from provider filtering). |

## Recovery query

When switching from provider `X` to `openai`:

```sql
UPDATE threads SET model_provider='openai', model=NULL WHERE model_provider='X';
```

## Other tables (supplementary)

- `thread_dynamic_tools` — per-thread tool registrations (FK → threads.id)
- `thread_spawn_edges` — subagent spawn relationships (parent/child threads)
- `stage1_outputs`, `jobs`, `agent_jobs`, `agent_job_items` — background task state
- `backfill_state`, `remote_control_enrollments`, `thread_goals` — feature flags/state
- `_sqlx_migrations` — schema migration history
