# 适配器文件格式参考

## Claude Code（~/.claude/skills.md）

```markdown
# Pakco 统一技能库索引

> 规范库路径: `~/.hermes/skills/`
> 读取方式: 用 Read 工具加载对应 SKILL.md
> 更新命令: `pakco-skills sync`

## <category>
- **<skill-name>** — <description> (→ `~/.hermes/skills/<category>/<name>/SKILL.md`)
```

引用注入位置：`~/.claude/CLAUDE.md`，在 `<!-- SKILLS_LIBRARY_START -->` 和 `<!-- SKILLS_LIBRARY_END -->` 标记之间。

## Codex（~/.codex/hermes-skills.md）

```markdown
# Pakco 统一技能库索引（Codex）

> 规范库路径: `~/.hermes/skills/`
> 读取方式: 用 read_file 工具加载对应 SKILL.md
> 更新命令: `pakco-skills sync`

## <category>
- **<skill-name>** — <description> (→ `~/.hermes/skills/<category>/<name>/SKILL.md`)
```

引用注入位置：`~/.codex/AGENTS.md`，同样的 HTML 注释标记。

## 未来 Agent

新增 Agent 时遵守同一模式：
1. 索引文件格式同上，适配各 Agent 的 Markdown 方言
2. 引用注入到该 Agent 的全局配置文件（通常是 `~/.<agent>/AGENTS.md` 或 `~/.<agent>/CLAUDE.md` 或 `~/.<agent>/rules/`）
3. 使用 `<!-- SKILLS_LIBRARY_START/END -->` 作为可替换块的边界标记
