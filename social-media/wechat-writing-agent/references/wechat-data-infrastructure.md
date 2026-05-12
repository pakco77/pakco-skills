# 公众号数据基础设施

> 乘百Pakco 公众号的自动化数据管线。本周报系统 + 内容审计脚本。

## 前置条件

**公众号 API 不可用**：乘百Pakco 是未认证订阅号（AppID: `wxbf95ceee503157d2`）。以下 API 全部返回 48001：
- `freepublish/batchget`
- `datacube/getarticletotal`
- `datacube/getusersummary`

认证（¥300/年）可全部解锁。当前走手动路线。

## 手动数据管线

### 用户操作（每周一次，2分钟）

1. 公众号后台 → 内容分析 → 群发数据
2. 右上角「导出 CSV」
3. 会下载 `tendency_<timestamp>.xls`（WPS 格式）
4. 扔到 `写作Agent/数据/` 目录

### 自动处理

脚本：`写作Agent/wechat_weekly.py`

```bash
python3 ~/Documents/Obsidian\ Vault/写作Agent/wechat_weekly.py
```

输出：`写作Agent/输出/周报-YYYY-MM-DD.md`

### 定时任务

Hermes cron：每周一 9:00 自动跑。

```
cron: 0 9 * * 1
job_id: 1567f46c347a
```

cron 做的事：
1. 扫描 `写作Agent/数据/` 下的 tendency XLS
2. 有新文件则解析 + 生成周报
3. 无新文件则提醒用户去后台导出

## 数据格式

### tendency XLS 结构（16列，722行）

| 区域 | 列 | 内容 |
|------|-----|------|
| 左侧 (1-3) | 日期, 渠道, 阅读人数 | 每日按渠道的阅读量（公众号消息/聊天会话/朋友圈/主页/其他/推荐/搜一搜/全部） |
| 中间 (5-9) | 日期, 分享人数, 原文阅读, 收藏人数, 发表篇数 | 每日互动数据 |
| 右侧 (11-14) | 传播渠道, 发表日期, 内容标题, 阅读人数, 阅读人数占比 | 文章级汇总 |

数据范围示例：2026.02.10-2026.05.10（90天）。

### user_analysis.xls

WPS Office 导出的 HTML 格式伪 XLS。pandas `read_html` 和 `read_excel` 均无法直接解析。**当前不处理此文件**（粉丝画像数据暂时跳过，等认证后用 API 自动拉）。

## 文件清单

```
写作Agent/
├── wechat_weekly.py          # 周报生成器
├── audit_pakco.py            # 内容审计（字数/论点/对抗/情绪/10万+基线）
├── 数据/                     # 用户手动放入 tendency XLS
├── 输出/
│   ├── 周报-YYYY-MM-DD.md    # 自动生成
│   └── audit_report.md       # 审计报告
└── .weekly_state.json        # 内部状态（增量计算用）
```

## 凭据

存于 `~/.hermes/.env`：
```
WECHAT_APPID=wxbf95ceee503157d2
WECHAT_APPSECRET=<已存>
```

IP 白名单：`113.78.93.3`（Hermes 云环境出口 IP，可能变更。变更后需在公众号后台重新添加）。
