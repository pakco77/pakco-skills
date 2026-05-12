#!/usr/bin/env python3
"""
乘百Pakco 公众号周报生成器
从公众号后台 tendency XLS → 周报 MD
"""
import pandas as pd
import re, os, json
from pathlib import Path
from datetime import datetime, timedelta

HOME = Path.home()
VAULT = HOME / "Documents/Obsidian Vault/写作Agent"
DATA_DIR = VAULT / "数据"
OUTPUT_DIR = VAULT / "输出"
ARTICLE_DIR = VAULT / "公众号"
STATE_FILE = VAULT / ".weekly_state.json"

def parse_tendency_xls(filepath):
    df = pd.read_excel(filepath, header=None)
    result = {'date_range': '', 'articles': [], 'daily_reads': [], 'daily_engage': [],
              'total_reads': 0, 'total_shares': 0, 'total_favs': 0}
    title_cell = str(df.iloc[0, 1]) if pd.notna(df.iloc[0, 1]) else ''
    m = re.search(r'(\d{4}\.\d{2}\.\d{2}).*?(\d{4}\.\d{2}\.\d{2})', title_cell)
    if m:
        result['date_range'] = f"{m.group(1)} ~ {m.group(2)}"
    articles_raw = df.iloc[2:, [11, 12, 13, 14]].copy()
    articles_raw.columns = ['渠道', '日期', '标题', '阅读量']
    articles_raw = articles_raw.dropna(subset=['标题'])
    articles = articles_raw[articles_raw['渠道'] == '全部'].copy()
    articles['阅读量'] = pd.to_numeric(articles['阅读量'], errors='coerce').fillna(0).astype(int)
    result['articles'] = articles[['日期', '标题', '阅读量']].to_dict('records')
    daily = df.iloc[2:, [1, 2, 3]].copy()
    daily.columns = ['日期', '渠道', '阅读量']
    daily = daily.dropna(subset=['日期'])
    daily['阅读量'] = pd.to_numeric(daily['阅读量'], errors='coerce').fillna(0)
    daily_all = daily[daily['渠道'] == '全部'].copy()
    result['daily_reads'] = daily_all[['日期', '阅读量']].to_dict('records')
    engage = df.iloc[2:, [5, 6, 7, 8, 9]].copy()
    engage.columns = ['日期', '分享', '原文阅读', '收藏', '发表']
    engage = engage.dropna(subset=['日期'])
    for c in ['分享', '原文阅读', '收藏', '发表']:
        engage[c] = pd.to_numeric(engage[c], errors='coerce').fillna(0)
    result['daily_engage'] = engage.to_dict('records')
    result['total_reads'] = sum(a['阅读量'] for a in result['articles'])
    result['total_shares'] = int(engage['分享'].sum())
    result['total_favs'] = int(engage['收藏'].sum())
    return result

def match_articles(articles, article_dir):
    md_files = {}
    if article_dir.exists():
        for f in article_dir.glob('*.md'):
            md_files[f.stem] = str(f)
    matched = []
    for a in articles:
        title = a['标题'].strip()
        best = None
        best_score = 0
        for stem, path in md_files.items():
            if title[:20] in stem or stem[:20] in title:
                score = len(set(title) & set(stem)) / max(len(title), len(stem))
                if score > best_score:
                    best_score = score
                    best = path
        a['md_path'] = best
        a['match_score'] = round(best_score, 2)
        matched.append(a)
    return matched

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(data):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def generate_report(data, prev_state):
    now = datetime.now()
    articles = match_articles(data['articles'], ARTICLE_DIR)
    prev_articles = {a['标题']: a for a in prev_state.get('articles', [])}
    lines = [f"# 乘百Pakco 周报", f"\n> 生成: {now.strftime('%Y-%m-%d %H:%M')}",
             f"> 数据范围: {data['date_range']}",
             f"> 文章总数: {len(articles)} 篇 | 总阅读: {data['total_reads']:,}",
             f"", "## 一、文章阅读量排行", "", "| # | 标题 | 阅读量 | MD |", "|---|------|:---:|:---:|"]
    for i, a in enumerate(sorted(articles, key=lambda x: x['阅读量'], reverse=True), 1):
        has_md = '✅' if a['md_path'] else '⬜'
        lines.append(f"| {i} | {a['标题'][:40]} | {a['阅读量']:,} | {has_md} |")
    if prev_state:
        lines.extend(["", "## 二、本周增量", "", "| 标题 | 上周 | 本周 | 增量 |", "|------|:---:|:---:|:---:|"])
        for a in articles:
            prev_reads = prev_articles.get(a['标题'], {}).get('阅读量', a['阅读量'])
            delta = a['阅读量'] - prev_reads
            icon = '📈' if delta > 0 else ('📉' if delta < 0 else '➡️')
            lines.append(f"| {a['标题'][:30]} | {prev_reads:,} | {a['阅读量']:,} | {icon} {delta:+,} |")
    lines.extend(["", "## 三、每日阅读趋势（近14天）", "", "| 日期 | 阅读 |", "|------|:---:|"])
    daily = data['daily_reads']
    recent = [d for d in daily if str(d['日期']).replace('-','') >= (now - timedelta(days=14)).strftime('%Y%m%d')]
    for d in recent[-14:]:
        lines.append(f"| {d['日期']} | {int(d['阅读量']):,} |")
    lines.extend(["", "## 四、互动", ""])
    publish_days = sum(1 for e in data['daily_engage'] if e['发表'] > 0)
    lines.append(f"- 发表: {publish_days}天 | 总分享: {data['total_shares']} | 总收藏: {data['total_favs']}")
    avg_share = data['total_shares'] / max(data['total_reads'], 1) * 100
    lines.append(f"- 分享率: {avg_share:.1f}%")
    lines.extend(["", "## 五、AI 洞察", ""])
    top = max(articles, key=lambda x: x['阅读量']) if articles else None
    if top:
        lines.append(f"🏆 「{top['标题']}」— {top['阅读量']:,} 阅读")
    missing = [a for a in articles if not a['md_path']]
    if missing:
        lines.extend(["", "⚠️ 缺少本地 MD:"])
        for a in missing:
            lines.append(f"- {a['标题']}（{a['阅读量']:,} 阅）")
    lines.extend(["", "### 📋 待办", "- [ ] 导出公众号后台 tendency CSV", "- [ ] 放入 `写作Agent/数据/`", "- [ ] 运行 `python3 wechat_weekly.py`"])
    return '\n'.join(lines)

def find_latest():
    if not DATA_DIR.exists():
        return None
    xls_files = sorted(DATA_DIR.glob('tendency_*.xls'), reverse=True)
    return str(xls_files[0]) if xls_files else None

def main(xls_path=None):
    if xls_path is None:
        xls_path = find_latest()
    if xls_path is None or not os.path.exists(xls_path):
        print("[X] 找不到 tendency XLS。请放入 写作Agent/数据/")
        return
    print(f"[~] 解析: {os.path.basename(xls_path)}")
    data = parse_tendency_xls(xls_path)
    prev = load_state()
    report = generate_report(data, prev)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    f = OUTPUT_DIR / f"周报-{datetime.now().strftime('%Y-%m-%d')}.md"
    f.write_text(report, encoding='utf-8')
    save_state({'last_run': datetime.now().isoformat(), 'articles': data['articles'], 'total_reads': data['total_reads']})
    print(f"[OK] {f}\n     文章: {len(data['articles'])} | 总阅读: {data['total_reads']:,}")

if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)
