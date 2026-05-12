---
name: pakco-writing-system
description: 乘百Pakco 公众号写作与运营系统——重启即用。涵盖：(1) 文章写作（Pakco/卡兹克/Hybrid 三模式）；(2) 数据审计（周报生成）；(3) 10万+诊断与改进；(4) 分发策略。触发词：重启写作Agent、公众号写作、pakco写作系统、公众号周报、写作审计。
---

# pakco-writing-system

> 乘百Pakco 公众号写作与运营系统。重启 Agent 时只需说「重启写作Agent」。

## 重启指令

告诉 Agent：**「重启写作Agent」或「加载 pakco-writing-system」**

Agent 会自动：
1. 扫描 Obsidian 写作目录确认上下文
2. 加载文风参考（Pakco + 卡兹克）
3. 检查最新周报数据
4. 进入待命状态

---

## 系统构成

```
写作Agent/
├── wechat_weekly.py          # 周报生成脚本
├── audit_pakco.py            # 内容审计脚本
├── 数据/                     # 从公众号后台导出的 tendency XLS
├── 公众号_已发/              # Pakco 历史文章 MD（27+ 篇）
├── 公众号_草稿/              # 草稿（2+ 篇）
├── 好文/                     # 参考文章（卡兹克等）
├── 输出/                     # 产出：新文章 MD/HTML、周报 MD、系统性复盘
├── Pakco文风分析.md          # 基于5篇完整语料分析
├── 卡兹克文风分析.md         # 卡兹克叙事技巧分析
├── 10万+差距诊断.md          # 10个差距与优先级
├── 系统性复盘-2026-05-11.md  # 全量数据分析复盘（in 输出/）
└── 灵感池.md / 一些思考.md   # 选题储备
```

关键路径（代码里用到）：
- Skill 目录：`~/.hermes/skills/social-media/wechat-writing-agent/`
- huashu-md-html 脚本：`~/.hermes/skills/huashu-md-html/scripts/md_to_html.py`
- Obsidian vault：`~/Documents/Obsidian Vault/写作Agent/`

---

## 能力一：写文章（三模式）

### 触发方式

```
「用我的风格写一篇关于XXX的」  → Pakco 模式
「用卡兹克风格写XXX」          → Kazel 模式
「融合风格写XXX」              → Hybrid 模式
```

### 工作流（5步）

1. **确认需求**：主题、模式、字数、特殊约束
2. **生成大纲**：按模式的结构公式出大纲 → 用户确认
3. **写正文 MD**：写入 `写作Agent/输出/`，文件名 `YYYY-MM-DD 标题.md`
4. **封面建议**：摘要 + 封面图方向
5. **HTML 预览**：用 huashu-md-html 的 reading 模板转换

```bash
python3 ~/.hermes/skills/huashu-md-html/scripts/md_to_html.py 输出.md --theme reading -o 输出.html
```

### 模式速查

| 模式 | 结构公式 | 开场 | 结尾 | 语气 |
|------|---------|------|------|------|
| **Pakco** | 钩子→展开→方法→升华→固定结尾 | 「Hi 朋友们，我是Pakco」 | 「谢谢你读到这里，无声感激。我是Pakco」 | 轻松、自嘲、产品经理视角 |
| **Kazel** | 钩子→引入路径→人物→方法→价值反转→升华 | 直接进故事 | 「以上……>/ 作者：XX」 | 沉稳克制、社会关怀 |
| **Hybrid** | Pakco开场→框架拆解→Kazel叙事深描→回归框架→升华→Pakco结尾 | Pakco式 | Pakco固定结尾 + 卡兹克署名 | 两种语气交替，不同段不能混 |

### 禁忌

- ❌ 不用「家人们」「宝子们」
- ❌ 不喊口号式结尾
- ❌ 不堆砌技术名词
- ❌ 删除「在当今这个日新月异的时代」「众所周知」

### 参考文件

| 文件 | 内容 |
|------|------|
| `references/quick-start.md` | 重启指令速查 |
| `references/10x-standards.md` | 10x打磨标准（70/90/95分层） |
| `references/wechat-data-guide.md` | 公众号后台数据解析 |
| `references/review-checklist.md` | 发布前审查清单 |

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/wechat_weekly.py` | 周报生成器（依赖 pandas, openpyxl） |

## 核心路径

- Obsidian vault：`~/Documents/Obsidian Vault/写作Agent/`
- 已发文章：`公众号_已发/`
- 草稿：`公众号_草稿/`
- 数据：`数据/`（放 tendency XLS）
- 输出：`输出/`（周报、文章 MD/HTML）
- 诊断文件：`10万+差距诊断.md`、`Pakco文风分析.md`、`卡兹克文风分析.md`
- Skill 目录：`~/.hermes/skills/pakco-writing-system/`

---

## 能力二：数据审计

### 生成周报

前提：用户已从公众号后台导出 tendency XLS 放入 `写作Agent/数据/`。

```bash
python3 ~/Documents/Obsidian\ Vault/写作Agent/wechat_weekly.py
```

输出：`写作Agent/输出/周报-YYYY-MM-DD.md`

### 内容审计

```bash
python3 ~/Documents/Obsidian\ Vault/写作Agent/audit_pakco.py
```

输出：`写作Agent/输出/audit_report.md`

### 定时任务

每周一 9:00 自动跑（cron job `1567f46c347a`）。

查看/管理：`hermes cron list`

### 如何获取数据

1. 公众号后台 → 内容分析 → 右上角「导出 CSV」
2. 把导出的 tendency_*.xls 放入 `写作Agent/数据/`
3. 运行脚本或等周一自动跑

---

## 能力三：10万+诊断

加载 `写作Agent/10万+差距诊断.md` 阅读完整分析。**系统复盘**见 `写作Agent/输出/系统性复盘-2026-05-11.md`（含27篇文章全量数据分析）。

**核心结论**：乘百Pakco 差在——
1. 🔴 选题在工具层（没穿透到命运层）
2. 🔴 观点太温和（转发需要锐度）
3. 🔴 情绪恒温（缺低谷→释放）
4. 🟡 对抗对象不清（防御型而非进攻型）
5. 🟡 全是 AI 内容（受众天花板低）

**对抗对象**：你在对抗「技术的光环」——技术门槛神话、工具消费主义、AI 万能论。

**改写标准**：70分→90分→95分。每轮聚焦一个维度。

---

## 能力四：样式提取 → HTML排版 → 推送草稿箱（发布流水线）

### 工具链

| 环节 | 工具 | 路径 |
|------|------|------|
| 提取样式 | wechat-typesetting | `~/wechat-typesetting/`（Next.js，`npm run dev`→`:3000`） |
| MD→HTML | pandoc + huashu-md-html | `~/.hermes/skills/huashu-md-html/` |
| 定制主题 | theme-pakco.css | `~/.hermes/skills/huashu-md-html/templates/wechat/theme-pakco.css` |
| 推送草稿 | wechat-typesetting API | `POST :3000/api/publish/draft` |

### 发布流水线（4步）

**前提**：wechat-typesetting 已配置 AppID/AppSecret（`POST /api/config`），dev server 已启动。

1. **提取样式**（可选，已有 theme-pakco 则跳过）
```bash
# 调 wechat-typesetting API 提取目标文章的样式基因
curl -X POST http://localhost:3000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/..."} '
```

2. **MD → HTML（套 Pakco 主题）**
```bash
pandoc "$MD" \
  --from markdown+smart+pipe_tables+task_lists+fenced_divs+bracketed_spans \
  --to html5 \
  --metadata title="$TITLE" \
  --metadata theme=wechat \
  --metadata author="乘百Pakco" \
  --metadata eyebrow="公众号 · 乘百Pakco" \
  --standalone \
  --css ~/.hermes/skills/huashu-md-html/templates/wechat/theme-pakco.css \
  --template ~/.hermes/skills/huashu-md-html/templates/wechat/template.html5 \
  -o "$OUT"
```

3. **内联 CSS**（让 HTML 自包含，不依赖外部文件）
```python
# 把 <link rel="stylesheet"> 替换为 <style>...</style>
html = re.sub(r'<link[^>]+theme-pakco\.css[^>]*>', f'<style>\n{css}\n</style>', html)
```

4. **推送到公众号草稿箱**
```python
POST http://localhost:3000/api/publish/draft
{
  "title": "...",
  "content": "<article>...</article>",  # 提取 body 内文章内容，去除 copy-bar/script
  "author": "乘百Pakco",
  "coverUrl": "http://localhost:3000/cover.png"  # 可选，不传则自动生成绿底封面
}
```

如果文章内有图片，API 会自动上传到微信图床并替换 URL。封面图可拷到 `~/wechat-typesetting/public/` 用 `http://localhost:3000/filename` 引用。

### Pakco 主题（theme-pakco.css）

提取自「Agent就该反省了」的实际样式：

| 属性 | 值 |
|------|-----|
| 主色 | `#C15F3C`（铁锈红） |
| 字体 | PingFang SC / 15px |
| 标题 | 22px bold 左对齐 |
| 分隔线 | 0.5px `rgba(0,0,0,0.1)` |
| 代码块 | `rgb(25,26,36)` 底白字 |
| 行高 | 1.6em |
| 表格 | 主色 8% 表头底 |

---

## 能力五：分发策略

### 渠道矩阵

| 渠道 | 频率 | 策略 |
|------|------|------|
| 少数派 | 每周1篇投稿 | 改标题→投稿→文末留公众号钩子 |
| 即刻 | 每日1条+3评论 | 发金句不是链接；认真评论别人 |
| 朋友圈 | 每篇3版导语 | 脆弱版/悬念版/金句版→让别人选 |

### 时间分配

```
写文章: 3小时
改标题+导语: 1小时  
分发: 1小时
```

---

## 重启时 Agent 自动做的事

1. 加载 `wechat-writing-agent` skill 获取完整写作方法论
2. `search_files` 检查 `写作Agent/公众号_已发/` 下文章数量
3. `search_files` 检查 `写作Agent/输出/` 下最新产出
4. `search_files` 检查 `写作Agent/数据/` 下最新 XLS
5. 如有新 XLS，自动跑 `wechat_weekly.py`
6. 检查 `~/wechat-typesetting/` 是否已安装，记录状态
7. 汇报：文章数、最新周报数据、发布工具状态、待办

---

## 能力五：样式提取与定制排版

### 从参考文章提取样式

用于：给 MD 套上对标文章/自己文章的视觉风格，生成可以直接粘贴到公众号编辑器的 HTML。

**步骤**：

1. 确保 wechat-typesetting 已启动：
   ```bash
   cd ~/wechat-typesetting && npm run dev &
   ```
   等待服务就绪（`http://localhost:3000`）。

2. 调用 API 提取样式（不能用 curl——Hermes 终端环境可能被 blocking；用 Python urllib）：
   ```python
   import urllib.request, json
   url = "http://localhost:3000/api/extract"
   data = json.dumps({"url": "https://mp.weixin.qq.com/s/XXXXX"}).encode()
   req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
   with urllib.request.urlopen(req) as resp:
       result = json.loads(resp.read())
   # result["styleProfile"] 包含完整的配色/字体/装饰信息
   ```

3. 根据 `styleProfile` 写一份定制 CSS（参考 `templates/theme-pakco.css`）放到：
   ```
   ~/.hermes/skills/huashu-md-html/templates/wechat/theme-<name>.css
   ```

4. 用 pandoc 套模板 + 定制 CSS 转换 MD：
   ```bash
   pandoc 文章.md \
     --from markdown+smart+pipe_tables+task_lists+fenced_divs+bracketed_spans \
     --to html5 \
     --metadata title="标题" --metadata author="乘百Pakco" \
     --metadata eyebrow="公众号 · 乘百Pakco" --metadata date="YYYY-MM-DD" \
     --standalone --css ~/.hermes/skills/huashu-md-html/templates/wechat/theme-<name>.css \
     --template ~/.hermes/skills/huashu-md-html/templates/wechat/template.html5 \
     -o 输出.html
   ```

5. 内联 CSS（pandoc 生成的是 `<link>` 外链，需替换为 `<style>` 块以自包含）：
   ```python
   import re
   with open('输出.html') as f: html = f.read()
   with open('theme-<name>.css') as f: css = f.read()
   html = re.sub(r'<link rel="stylesheet" href="[^"]+theme-<name>\.css"[^>]*>', f'<style>\n{css}\n</style>', html)
   with open('输出.html', 'w') as f: f.write(html)
   ```

6. 输出 HTML 自带「复制到公众号」按钮——浏览器打开，点一下即无损粘贴到公众号编辑器。

### 已有定制主题

| 主题 | CSS 路径 | 来源 |
|------|---------|------|
| theme-pakco | `~/.hermes/skills/huashu-md-html/templates/wechat/theme-pakco.css` | 提取自 Pakco「Agent就该反省了」 |
| (新建) | `~/.hermes/skills/huashu-md-html/templates/wechat/theme-<name>.css` | 按需新建 |

### 定制 CSS 模板

本 skill 自带一份可复用的模板：`templates/theme-pakco.css`（基于提取结果的标准结构，改颜色/字体即可派生新主题）。

---

## 工具链

| 环节 | 工具 |
|------|------|
| 写 MD | Agent 直接生成 |
| MD→HTML（阅读） | huashu-md-html reading 模板 |
| MD→HTML（公众号排版） | pandoc + theme-pakco.css + wechat 模板 |
| 样式提取 | wechat-typesetting（`~/wechat-typesetting/`） |
| 推草稿箱 | wechat-typesetting publish API |
| 数据解析 | wechat_weekly.py（依赖 pandas, openpyxl） |
| 定时 | Hermes cron |
| 记忆 | Obsidian vault（文件即记忆） |
| 数据解析 | wechat_weekly.py（依赖 pandas, openpyxl） |
| 定时 | Hermes cron |
| 记忆 | Obsidian vault（文件即记忆） |

### wechat-typesetting（公众号排版与推送）

路径：`~/wechat-typesetting/` | 启动：`cd ~/wechat-typesetting && npm run dev` → `http://localhost:3000`

三个能力：
1. **样式提取** — 粘贴公众号文章链接，自动提取配色/字体/装饰模式
2. **Markdown 排版** — 选模板后将 MD 转成公众号兼容 HTML（内联样式）
3. **推送草稿箱** — 配置 AppID+AppSecret 后一键推到公众号草稿箱

工作流衔接：
- 预览：写完 MD → huashu-md-html reading 模板
- 排版发布：写完 MD → 提取参考样式 → 定制 CSS → pandoc 转 HTML → 浏览器打开 → 点「复制到公众号」粘贴
