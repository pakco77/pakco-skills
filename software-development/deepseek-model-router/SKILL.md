---
name: deepseek-model-router
description: "智能任务分类路由：根据任务复杂度自动选择 v4-flash（简单）/ v4-pro（默认）/ GPT-5.5（高难）。2026年5月31日前 v4-pro 有大幅折扣，设为默认。"
version: 1.0.0
author: Pakco
metadata:
  trigger_on: task_classification
  default_model: deepSeek-v4-pro
  discount_deadline: "2026-05-31"
---

# DeepSeek 模型智能路由器

根据任务复杂度自动将任务分流到最合适的模型，在成本和效果之间取得平衡。

**核心理念**：不是所有任务都需要最强大脑。简单任务用 flash（快+便宜），日常任务用 pro（默认，大折扣期），硬骨头才上 GPT-5.5。

---

## 三档模型速查

| 档位 | 模型 | Provider | 适用场景 | 特点 |
|------|------|----------|----------|------|
| 🚀 L1 轻量 | `deepseek-chat` | `deepseek` | 简单问答、翻译、小段代码解释、格式化、闲聊 | 最快最便宜 |
| ⚡ L2 默认 | `deepSeek-v4-pro` | `zeoapi` | **大部分日常任务**（开发、调试、研究、写作、工具编排） | **当前默认**（5月31日前大折扣） |
| 🧠 L3 重型 | `GPT-5.5` | `zeoapi` | 架构设计、复杂多步推理、硬核调试、系统级设计 | 最强大但也最贵 |

> ⚠️ **时间敏感**：2026年5月31日前 v4-pro 有大幅折扣，此后需重新评估默认模型。

---

## 分类决策树

收到用户任务时，按以下维度打分（每项 0-2 分），总分决定档位：

### 评分维度

1. **推理深度**：是否需要多步逻辑链、数学推导、复杂因果关系？
   - 0：不需要推理 / 1：需要2-3步推理 / 2：需要深层多步推理

2. **代码复杂度**：是否涉及多文件、架构决策、算法设计？
   - 0：不涉及代码 / 1：单文件编辑 / 2：多文件重构、架构级改动

3. **领域专业度**：是否需要跨领域知识或深度专业判断？
   - 0：通用知识 / 1：单一专业领域 / 2：跨领域综合

4. **输出质量要求**：对准确性、完整性、格式的容忍度？
   - 0：随便 / 1：要求准确但不严格 / 2：零容忍（生产代码、正式文档）

5. **工具调用密度**：预计需要多少轮工具调用？
   - 0：0-1轮 / 1：2-5轮 / 2：6+轮

### 总分 → 档位

| 总分 | 档位 | 模型 |
|------|------|------|
| 0-3 | L1 | `deepseek-chat` (v4-flash) |
| 4-7 | **L2（默认）** | **`deepSeek-v4-pro`** |
| 8-10 | L3 | `GPT-5.5` |

### 快速判断口诀

- 「能秒答的」→ flash
- 「需要想想的」→ **pro（默认）**
- 「需要开动脑筋的」→ GPT-5.5

---

## 执行方式

### 方式一：推荐切换（会话开始/任务开始）

当加载此 skill 后，收到用户任务的**第一个消息**时：

1. 用上面的维度打分
2. 对照当前会话使用的模型
3. 如果匹配 → 直接执行
4. 如果不匹配 → 回复中**先给出分类结果 + 推荐切换命令**，再在当前模型下执行

示例回复模板：
```
📊 任务分类：L1 轻量 → 推荐 v4-flash
当前在用 v4-pro，建议切模型节省成本：
  hermes config set model.default deepseek-chat
  hermes config set model.provider deepseek
然后 /reset 开始新会话。
（本次先用 v4-pro 继续……）
```

### 方式二：分批处理（切换模型跑批）

当你有**一批同类轻量任务**（翻译、格式化、简单问答）或**一个硬仗任务**时，
不要在当前会话里混着做——先切模型、开新会话批量处理，再切回来。

```bash
# 场景A：攒了一堆简单任务 → 切 flash 批量跑
hermes config set model.default deepseek-chat
hermes config set model.provider deepseek
hermes  # 新会话，批量处理轻量任务
# 跑完后：
hermes config set model.default deepSeek-v4-pro
hermes config set model.provider zeoapi

# 场景B：遇到硬骨头 → 切 GPT-5.5 单独开会话
hermes config set model.default GPT-5.5
hermes config set model.provider zeoapi
hermes  # 新会话，专心啃硬仗
# 啃完后切回 pro
```

**核心原则**：不要在一个会话里来回切模型（切了也不生效）。一个会话 = 一个模型，任务类型不匹配就新开会话。

### 方式三：全局默认切换

```bash
# 切到 v4-flash（轻量日）
hermes config set model.default deepseek-chat
hermes config set model.provider deepseek

# 切回 v4-pro（默认）
hermes config set model.default deepSeek-v4-pro
hermes config set model.provider zeoapi

# 切到 GPT-5.5（硬仗）
hermes config set model.default GPT-5.5
hermes config set model.provider zeoapi
```

**注意**：模型切换后需要 `/reset` 或新会话才生效。

---

## 典型场景速查

| 用户任务 | 分类 | 推荐模型 | 原因 |
|----------|------|----------|------|
| 「这个错误是什么意思」 | L1 | flash | 简单问答 |
| 「帮我翻译这段文字」 | L1 | flash | 翻译任务 |
| 「review 这个 PR」 | L2 | **pro** | 需要理解代码上下文 |
| 「写一个 REST API 接口」 | L2 | **pro** | 日常开发 |
| 「设计一个微服务架构」 | L3 | GPT-5.5 | 架构设计 |
| 「这个 bug 我调了三天，帮我看看」 | L3 | GPT-5.5 | 硬核调试 |
| 「重构整个认证模块」 | L3 | GPT-5.5 | 多文件重构 |
| 「写一篇文章」 | L2 | **pro** | 内容创作 |
| 「帮我规划下个月的学习路线」 | L2 | **pro** | 需要推理但不极端 |

---

## 降级策略

当推荐模型不可用时：
1. L1 不可用 → 用 L2（pro）继续
2. L2 不可用 → 用 L1（flash）应急，告知用户「pro 暂不可用，先用 flash 处理，可能质量略低」
3. L3 不可用 → 用 L2（pro）尝试，**明确告知用户**「GPT-5.5 不可用，用 v4-pro 处理，复杂推理可能不足」

---

## 2026年5月31日后

折扣结束后需重新评估：
1. 如果 v4-pro 恢复原价且与 GPT-5.5 价差缩小 → 考虑调整分类阈值
2. 如果 flash 性价比突出 → 可能提升 flash 的适用范围
3. **建议届时提醒用户重新 review 此 skill 的评分标准**

---

## 配置依赖

确保以下 env 已配置：
- `DEEPSEEK_API_KEY` → `.env` 中已配置 ✅
- `ZEO_API_KEY` → `.env` 中已配置 ✅

Provider 配置（config.yaml）：
```yaml
providers:
  deepseek:
    base_url: https://api.deepseek.com
    api_key_env: DEEPSEEK_API_KEY
    api_mode: chat_completions
  zeoapi:
    base_url: https://www.zeoapi.com/v1
    api_key_env: ZEO_API_KEY
    api_mode: chat_completions
```
