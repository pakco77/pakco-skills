---
name: unified-skill-library
description: "管理跨 Agent（Hermes / Claude Code / Codex）的统一技能库。一个 Git 仓库 = 唯一技能源，一套 SKILL.md 格式，多 Agent 通过适配器消费。触发词：统一技能、pakco-skills、技能库管理、跨 Agent 技能、技能同步。"
version: 1.0.0
created: 2026-05-12
---

# 统一技能库管理

## 架构

三层结构，一个 Git 仓库：

```
Agent Adapters（适配器层）
  Hermes（原生）· Claude Code（~/.claude/skills.md）· Codex（~/.codex/hermes-skills.md）
       ↑                    ↑                    ↑
Sync & Version（同步层）
  Git 仓库 · pakco-skills CLI · 多机 push/pull
       ↑
Canonical Store（规范库）
  ~/.hermes/skills/  —  218+ 技能，SKILL.md 格式
```

## 触发条件

用户提到：
- 「统一技能」「技能库管理」「跨 Agent 技能」
- 「pakco-skills」
- 「把技能同步到 Claude Code / Codex」
- 「新建技能」

## CLI 命令

```bash
pakco-skills sync        # 扫描所有 SKILL.md → 生成 Claude Code / Codex 适配器
pakco-skills new <name>  # 创建新技能骨架（在 ~/.hermes/skills/ 下）
pakco-skills list [cat]  # 列出所有技能，可选分类过滤
pakco-skills push        # git push 到 GitHub
pakco-skills pull        # git pull 拉取更新
```

脚本位置：`~/.hermes/scripts/pakco-skills`（软链接到 `~/bin/pakco-skills`）

## 添加新 Agent

1. 创建一个 `_gen_<agent>_index()` 函数，生成适合该 Agent 的索引文件
2. 创建一个 `_update_<agent>_config()` 函数，在 Agent 配置文件中注入技能库引用
3. 在 `cmd_sync()` 中调用这两个函数

适配器文件命名规范：`~/.<agent>/skills.md` 或 `~/.<agent>/hermes-skills.md`

适配器内容：分类 + 技能名 + 描述 + 路径引用，引导 Agent 用 Read 工具按需加载。

## 新建技能流程

1. `pakco-skills new <name> [category]` — 创建 SKILL.md 骨架
2. 编辑 `~/.hermes/skills/<category>/<name>/SKILL.md`
3. `pakco-skills sync` — 同步到所有 Agent
4. `git add/commit/push` — 版本管理

## 注意事项

- **不复制技能内容**到适配器——适配器只做索引引用，Agent 通过 Read 工具实时加载最新 SKILL.md
- **HERMES 原生无需适配**——技能放在 `~/.hermes/skills/` 下即自动发现
- **macOS sort 兼容**：脚本内用 `LC_ALL=C sort` 避免非 ASCII 字符导致的 "Illegal byte sequence" 错误
- **不用 pyyaml**：脚本用 `sed` 解析 YAML frontmatter，无 Python 依赖
- **PATH**：确保 `~/bin` 在 PATH 中（脚本在首次运行 sync 时添加）
- **嵌套 Git 仓库**：如果 `~/.hermes/skills/` 内有其他 Git 仓库（如 huashu-md-html），会被警告但功能正常——可后续转为 submodule
