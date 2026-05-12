# Resuming the Claude + CAM Agent Team

Use this reference when the user asks to “启动这个Agent team” or resume work from `/Users/pakco/Desktop/Claude + CAM/0_Agents team`.

## Active workspace

User-provided workspace path takes priority over older Obsidian paths:

`/Users/pakco/Desktop/Claude + CAM/0_Agents team`

Key files to read first:

1. `0_S_背景级资料/001_S_规则/1_系统级上下文.md`
2. `1_A_Agent角色提示词/0_PMO.md`
3. `0_S_背景级资料/002_S_产品方针/pakco与claude首次讨论.md`
4. `2_B_迭代冻结产出/0_迭代冻结产出/_product/genmitsu-cam-mvp-roadmap.md`
5. Latest feature folders under `2_B_迭代冻结产出/0_迭代冻结产出/`
6. Existing `2_B_迭代冻结产出/原型.html`

## Resume pattern

Do not restart from zero if B-level outputs already exist. Reconstruct state by checking which artifacts exist per feature:

`roadmap → constraints-v1 → prd → constraints-v2 → ux → ui → fe-verification → qa/beauty reports`

Then continue from the first missing artifact in the standard PMO pipeline.

## Session-specific finding from 2026-05-10

At that point:

- F001 had Roadmap / constraints / PRD / UX / UI / FE verification.
- F000 had Roadmap / constraints / PRD / UX, but lacked `F000-ui.md`.
- The right continuation was to dispatch UI for F000 before FE.
- `F000-ui.md` was created with 25 `--home-*` variables, no BREAKING changes, and 16 covered components.
- `F000_Home首页/log.md` was created to record PMO/UI status changes.

Later user裁决 in the same resume session:

- Do not overwrite the old prototype. Final GPT-5.5-run prototype output must be saved as `2_B_迭代冻结产出/原型(GPT5.5).html`; keep `原型.html` as old/reference output.
- Return to PMO Socratic before continuing FE.
- First-entry strategy = C: Home is onboarding Step 0. Keep “我的项目 + 社区作品”, but the primary CTA must explicitly lead to first-carving onboarding (“开始第一次雕刻” direction), with downstream L1/F000/F011 patches needed.

## Resume under context compaction

If `/resume <session_id>` does not recover useful state but the user provides a compaction summary or preserved todo list, treat that summary as the active resume index.

Recommended order:

1. Read only the target files named in the summary/todo list.
2. Verify whether the target artifact was actually written yet.
3. If the user asks for progress, answer from file evidence first (e.g. “roadmap and patch summary read; target PRD sibling exists but rewrite not yet written”).
4. Then continue execution from the first missing concrete artifact.

## Pitfalls

- Do not treat old Obsidian paths as authoritative when the user gives the Desktop workspace path.
- Do not ask the user to restate decisions already present in `pakco与claude首次讨论.md` or the L1 Roadmap.
- Do not inject full upstream documents into downstream agents; keep SABC trimming.
- F000 has 0🔴/0🟡 hardware constraints, so there is no yellow-light user裁决 before UX/UI.
- F000 community section is a mock: require “社区作品（即将上线）”, “以下为示例展示，敬请期待”, visible “示例” badge on every card, and no real CTA.
- When the user asks to go back to PMO Socratic, stop pipeline execution, record裁决 in `_product/log.md`, and ask one product-direction question at a time.
- When the active task is a document rewrite, do not imply progress from context gathering alone; verify whether the target file was actually updated and report that explicitly.
