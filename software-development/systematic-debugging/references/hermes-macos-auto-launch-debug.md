# Hermes macOS 自动启动 / 对话框弹出问题调试

## 适用场景

Hermes CLI/TUI 在没有用户输入的情况下自动启动、弹出新对话框/窗口，或反复创建空会话。常见于 macOS 系统。

## 系统级启动机制排查清单

按优先级排列，逐一排除：

### 1. Hermes 内部定时任务
```bash
cronjob list            # Hermes 内建的 cron 调度
```

### 2. macOS crontab
```bash
crontab -l              # 用户级 crontab
```

### 3. macOS launchd plists（最常见外部触发源）
```bash
# 搜索所有包含 hermes 的 plist
find ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons \
  -name "*.plist" | xargs grep -li "hermes" 2>/dev/null

# 查看所有用户级 LaunchAgent
ls ~/Library/LaunchAgents/
```

### 4. Shell 配置文件的自启动命令
```bash
for f in ~/.zshrc ~/.bashrc ~/.zprofile ~/.bash_profile ~/.profile; do
  [ -f "$f" ] && echo "=== $f ===" && grep -n "hermes\|hermes" "$f"
done
```

**注意自引用别名陷阱：**
```bash
alias hermes="cd ~/hermes-agent && source venv/bin/activate && hermes"
# ↑ 别名内又调用了 hermes，如果别名递归展开会出问题
```

### 5. macOS 登录项（Login Items）
```bash
osascript -e 'tell application "System Events" to get the name of every login item'
```

### 6. tmux / screen 守护会话
```bash
tmux list-sessions 2>/dev/null
screen -ls 2>/dev/null
```

### 7. Terminal.app 窗口恢复状态
```bash
# 检查是否保存终端窗口状态（重启后在原窗口恢复运行中的命令）
defaults read com.apple.Terminal NSQuitAlwaysKeepsWindows
# 检查终端启动配置
defaults read com.apple.Terminal "StartupWindowSettings"
```

### 8. macOS 快捷指令（Shortcuts）自动化
```bash
ls ~/Library/Shortcuts/
```

### 9. 日历自动化 / 提醒事项
```bash
sqlite3 ~/Library/Calendars/Calendar.sqlite \
  "SELECT title,summary FROM CalendarItem WHERE summary LIKE '%hermes%' OR title LIKE '%hermes%'"
```

### 10. 正在运行的 Hermes 进程
```bash
ps aux | grep -i hermes | grep -v grep
# 检查是否有多个 hermes 进程
```

### 11. 网络监听（是否有 gateway 在自动接受连接）
```bash
lsof -i -P 2>/dev/null | grep -i hermes
```

## Hermes 内部排查

### 检查 Hermes 会话数据库
```bash
sqlite3 ~/.hermes/state.db \
  "SELECT id, datetime(started_at,'unixepoch'), message_count, title \
   FROM sessions ORDER BY started_at DESC LIMIT 30;"

# 查看 Hermes 会话表结构
sqlite3 ~/.hermes/state.db ".schema sessions"
```

### 检查 Hermes 日志
```bash
cat ~/.hermes/logs/agent.log      # 代理运行日志
cat ~/.hermes/logs/errors.log     # 错误日志（不含 INFO）
# 查看最近错误
tail -50 ~/.hermes/logs/agent.log
```

### 检查 macOS 崩溃报告
```bash
ls -lt ~/Library/Logs/DiagnosticReports/hermes* 2>/dev/null
```

## 常见根因

| 现象 | 可能原因 | 检查方法 |
|------|---------|---------|
| 凌晨自动弹出多个对话框 | `session_reset.at_hour` 配置（默认4AM）或系统定时任务 | 检查 config.yaml `session_reset` 段 |
| 最小化 Terminal 后弹出对话框 | macOS 警示 "Terminal 要终止运行中的进程"；或 Terminal.app 窗口恢复功能 | 查看对话框文字、检查 Terminal 偏好设置 |
| 终端打开/重启后自动启动 Hermes | shell rc 文件或 launchd plist | 检查 rc 文件和 LaunchAgents |
| 反复弹出 Hermes 空白会话 | 有多个 hermes 进程在后台；或 gateway 在自动接收消息 | `ps aux \| grep hermes` |
| 对话框提示 API key 错误 | 辅助 LLM 客户端（session_search 等）使用了无效的 API key | 检查 `~/.hermes/.env` 和辅助模型配置 |

## 临时解决方案

如果急需让 Hermes 停止反复弹窗：

```bash
# 1. 杀死所有 hermes 进程
pkill -f hermes

# 2. 临时禁用 session_reset（如果是定时重置导致的问题）
# 在 config.yaml 中设置：
# session_reset:
#   mode: disabled

# 3. 检查并移除自启动项
# 如发现 ~/Library/LaunchAgents/ 中有 hermes 相关的 plist，备份后移走
```
