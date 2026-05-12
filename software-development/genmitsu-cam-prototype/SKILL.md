---
name: genmitsu-cam-prototype
description: "Genmitsu CAM 产品原型 Agent Team：Harness Engineering 原则下的 9 节点 Agent 协作系统。当前原型 v0.2：Home页+Wizard 4步+胶囊画布(2D/3D分屏+项目标签)。"
version: 3.3.0
---

# Genmitsu CAM 产品原型 Agent Team

## 概述

遵循 **Harness Engineering** 原则设计的多 Agent 协作系统。不是让 AI 一次做完所有事，而是设计套件（harness）——决定存储什么、检索什么、展示给模型什么。

**三条铁律：**
- 文件即记忆
- 隔离即常态
- 记录即保险

**核心设计文档（Obsidian）：** `/Users/pakco/Documents/Obsidian Vault/0_Genmitsu/0_Agents team 思考工程/`

> ⚠️ **Agent Team 路径灵活性**：Agent Team 文件可能存在于不同位置，不仅仅是 Obsidian vault。用户可能从其他路径（如 `Desktop/Claude + CAM/0_Agents team`）启动。**工作目录以用户提供为准**，不要硬编码回 Obsidian 路径。首次接入时先搜索文件结构以确认当前活跃路径。

---

## 节点结构（9 Agent）

```
用户点子 → [PMO] Socratic剖析 → [DA] Roadmap → 用户确认 → [HW P1] 约束v1 →
[PRD] PRD → [HW P2] 约束v2 → 黄灯裁决 → [UX] 骨架 → [UI] 规范 → [FE] 原型 →
[FQA + VQA] 并行双测试 → 用户验收
                │                    │
         闭环A (功能)          闭环B (美观)
```

## Agent 角色与文件（A 级提示词全部已写）

| # | 简称 | 中文角色 | 职责 | A 级文件 |
|---|------|---------|------|---------|
| 0 | **PMO** | 编排者 | 拆任务、管状态、上下文裁剪(SABC)、中转信息、维护需求清单状态字段 | `0_PMO.md` |
| 1 | **DA** | 需求解析 | 阶段识别(0→1/1→2/小需求)、Roadmap(系统级/版本级/功能级) | `1_DA.md` |
| 2 | **HW** | 硬件约束 | 两轮验证(P1轻量+P2细节)、红绿灯(🔴🟡🟢)、硬件关联预判 | `2_HW.md` |
| 3 | **PRD** | PRD撰写 | 三档PRD(完整/增量/微)、用户故事+验收标准+组件树、新增需求清单行 | `3_PRD.md` |
| 4 | **UX** | 交互设计 | 信息架构/页面流转/状态切换、新手极简Wizard路径 | `4_UX.md` |
| 5 | **UI** | 视觉设计 | CSS Custom Properties、组件状态规格、白底工业工具+Genmitsu绿VI | `5_UI.md` |
| 6 | **FE** | 前端工程 | 单文件HTML原型、增量集成、验收标准映射 | `6_FE.md` |
| 7 | **FQA** | 功能测试 | 7维功能审查(验收/交互/状态/边界/错误/键盘/跨feature)，代码只读 | `7_FQA.md` |
| 8 | **VQA** | 美观测试 | 7维美观审查(配色/边框/质感/氛围/动画/微光/装饰)，代码只读 | `8_VQA.md` |

> 所有 A 级文件路径：`1_A_Agent角色提示词/`

## 关键设计决策

- **SABC 上下文管理**：S(系统铁律+红绿灯+SABC规则本身) → A(Agent自身prompt) → B(冻结产出,PMO裁剪后注入下游) → C(过程草稿,仅自己可见)
- **红绿灯约束**：🔴硬约束(物理极限,不可挑战) → 🟡惯例约束(HW判定后用户裁决) → 🟢自由
- **显式上下文边界**：每个 Agent 明确声明可见/不可见范围；PMO 做片段裁剪不注全文
- **STALE 标记**：上游修改后下游自动标记失效；闭环完成后清除
- **上下文摘要层 + Diff 通知**：PMO 对 B 级文档做相关片段提取；闭环修补时给 diff 而非全量
- **回溯机制**：每个 Agent 每轮产出后提交改进计划到 `2_回溯报告/`
- **3 个用户介入点**：Roadmap确认 → 黄灯裁决 → HTML验收
- **3 阶段需求分流**：0→1(全链路) / 1→2(增量) / 小需求(快速通道,跳HW(P2))

## 文件组织

```
0_S_背景级资料/
├── 001_S_规则/
│   ├── 0_Agents工作流设计说明.md  ← 完整工作流设计
│   ├── 1_系统级上下文.md          ← S级上下文(全Agent注入)
│   └── 3_Skills.md                ← 参考技能清单
├── 002_S_产品方针/
├── 003_S_市场调研/
└── 004_S_硬件产品参数/
    └── Genmitsu_CNC_硬件参数表.md  ← 23款活跃机型全参数(HW Agent主参考)

1_A_Agent角色提示词/
├── 0_PMO.md  ← 编排者
├── 1_DA.md   ← 需求解析
├── 2_HW.md   ← 硬件约束
├── 3_PRD.md  ← PRD撰写
├── 4_UX.md   ← 交互设计
├── 5_UI.md   ← 视觉设计
├── 6_FE.md   ← 前端工程
├── 7_FQA.md  ← 功能测试
└── 8_VQA.md  ← 美观测试

2_B_迭代冻结产出/
├── 0_迭代冻结产出/
│   ├── CAM需求清单.xlsx        ← 唯一需求清单(PRD新增行/PMO更新状态)
│   └── [feature]/
│       ├── [feature]-roadmap.md
│       ├── [feature]-constraints-v1.md
│       ├── [feature]-prd.md
│       ├── [feature]-constraints-v2.md
│       ├── [feature]-ux.md
│       └── [feature]-ui.md
├── 原型.html                   ← 唯一原型文件（默认名；用户可能指定其他名称如 原型(GPT5.5).html，以最新为准）
├── 1_已发现问题收集/            ← FQA/VQA报告(按日期)
└── 2_回溯报告/                  ← 各Agent回溯报告
```

## 需求清单写入分工

| 写入者 | 列范围 | 时机 |
|-------|--------|------|
| **PRD** | A-E + L + M（新增行） | 每次产出 PRD 后 |
| **PMO** | F-K + N + O（状态字段） | 工作流流转中持续更新 |
| **其他 Agent** | — | 不读不写 |

## 已知设计问题

1. ✅ **PMO pipeline 分叉已修**：PMO 提示词新增「收到 DA 阶段判定后分叉」节，小需求正确跳过 HW(P2)。
2. **跨 feature STALE 通知缺失**：当 feature A 的 UX 改动影响 feature B 共享组件时，无自动通知机制。（优先级低，当前 feature 通常独立）
3. ✅ **硬件参数已补全**：`Genmitsu_CNC_硬件参数表.md` 含 23 款活跃机型全维度参数，S 级上下文含 9 款速查表。

## 测试验收记录（2026-05-09）

三阶段各一次测试，全链路通过：

| 测试 | 阶段 | 场景 | FQA | VQA | 闭环 | 最终 |
|------|------|------|-----|-----|------|------|
| 1 | 0→1 | 自动刀路新模块 | FAIL(4) | FAIL(3) | 🔄闭环B→FE修 | ✅ |
| 2 | 1→2 | 刀路时间预估增量 | FAIL(1) | PASS | 🔄FE单修 | ✅ |
| 3 | 小需求 | 导出按钮空反馈 | PASS | PASS | 无需闭环 | ✅ |

关键验证结论：SABC 隔离有效、红绿灯正确引用硬件参数、三阶段分流准确、双测试零重叠、微闭环归属判定正确。

## 使用方式

在 Hermes 对话中说一句话需求，PMO 自动走完 Socratic 对话 → 派发子代理 → 产出原型。用户介入点：Roadmap确认 → 黄灯裁决 → HTML验收。

> **与 brainstorming 技能的关系**：当用户在 Hermes 中提出产品级需求时，`brainstorming` 技能的 Socratic 对话由 PMO 角色承接执行——PMO 本身就是设计来与用户做苏格拉底式推敲的。不需要先跑 brainstorming 再切 Agent Team，直接走 PMO Socratic → DA Roadmap 即可。brainstorming 的"先设计再实现"硬 gate 已内化在 PMO→DA→用户确认→继续 的工作流中。

> **补丁方案整理触发条件**：如果 PMO 苏格拉底阶段已经锁定了一批会同时影响多个冻结文档的裁决（典型如 L1/F000/F011），不要立刻逐份改文档。先扫描当前冻结文档口径，输出一份 `_product/YYYY-MM-DD-...-patch-summary.md` 补丁摘要，再追加 `_product/log.md`，最后按 `L1 → F000 PRD → F000 UX/UI → F011` 的顺序派发修订。详见 `references/patch-summary-workflow.md`。
>
> **新旧文档区分**：如果用户要求区分新旧版本，不要覆盖已有冻结文档；应在同目录新建 sibling 副本，并加明确后缀（如 `_GPT5.4xh`）区分旧版，再把该副本作为后续修订目标。
>
> **日志写入纪律**：修改 `_product/log.md` 前先重读整份文件，不要只靠分页片段就直接 patch；若工具提示 sibling subagent / partial-read warning，先完整读文件再写，避免覆盖其他并行改动。

## 参考文件
## 参考文件

- `references/product-architecture-v0.2.md` — v0.2 产品架构（首页/Wizard/胶囊画布/2D-3D分屏）
- `references/home-step0-gpt55-session.md` — GPT-5.5 接管会话新增裁决：Home=新手引导 Step 0、双 CTA、首雕 Step 1/2 冻结、补丁方案整理、另存 `原型(GPT5.5).html`
- `references/patch-summary-workflow.md` — 当多份冻结文档同时受新裁决影响时，先产出补丁摘要再派发正式修订
- `references/prototype-first-iteration.md` — 当用户明确要求“以原型落地为最终目标”且接受按 feature 分批推进时，采用文档最小修订 + 原型分批落地的节奏
- `references/testing-methodology.md` — 三阶段测试方法论与典型问题
- `references/excel-to-markdown-pattern.md` — Excel 宽表转 Markdown 技术参考
- `references/project-context.md` — 项目背景与竞品分析
- `references/sabc-context-management.md` — SABC 上下文管理详细说明
