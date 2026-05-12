#!/usr/bin/env python3
"""
乘百Pakco 公众号内容审计脚本 v1.0
用法: python3 audit_pakco_content.py
输出: 终端报告 + audit_report.md（写入输出目录）

扫描 Obsidian 写作Agent/公众号/ 下所有 .md 文件，
提取: 字数、论点句、对抗句式、情绪指标，
生成逐篇分析报告 + 与10万+基线差距。
"""
import os
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

VAULT_PATH = Path.home() / "Documents/Obsidian Vault/写作Agent/公众号_已发"
OUTPUT_DIR = Path.home() / "Documents/Obsidian Vault/写作Agent/输出"
OUTPUT_FILE = OUTPUT_DIR / "audit_report.md"

def parse_frontmatter(text):
    meta = {}
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line:
                key, _, val = line.partition(':')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                meta[key] = val
    return meta

def strip_markdown(text):
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\([^)]+\)', '', text)
    text = re.sub(r'[>\-*] ', '', text)
    text = re.sub(r'[/\-]{3,}', '', text)
    return text.strip()

def extract_thesis(text):
    markers = ['真正', '本质', '核心', '不需要', '没必要', '不应该',
               '关键', '其实', '但', '然而', '问题是', '可惜']
    pure = strip_markdown(text)
    sentences = re.split(r'[。！？\n]', pure)
    results = []
    for s in sentences:
        s = s.strip()
        if 10 < len(s) < 150 and any(m in s for m in markers):
            results.append(s)
    return results

def find_against_patterns(text):
    pure = strip_markdown(text)
    return re.findall(
        r'(?:不是|不该|不要|不需要|没必要)[^。！？\n]{3,80}(?:而是|是|才是)[^。！？\n]{3,50}',
        pure
    )

def analyze_emotion(text):
    pos = len(re.findall(r'(喜欢|好|厉害|强|快|方便|舒服|简单|免费|感激|感谢|棒|妙|完美|惊喜|成功|赢)', text))
    neg = len(re.findall(r'(失败|丑|累|苦|难|焦虑|怕|担心|不敢|不足|差|烂|崩溃|烦|遗憾|丢人)', text))
    self_w = len(re.findall(r'我[^们]', text))
    we_w = len(re.findall(r'我们|大家|每个人|所有人|任何人', text))
    return {'positive': pos, 'negative': neg, 'self_ref': self_w, 'we_ref': we_w,
            'we_ratio': we_w / max(self_w, 1)}

def main():
    if not VAULT_PATH.exists():
        print(f'[X] 目录不存在: {VAULT_PATH}')
        return
    articles = []
    for md_file in sorted(VAULT_PATH.glob('*.md')):
        text = md_file.read_text(encoding='utf-8')
        meta = parse_frontmatter(text)
        title = meta.get('title', md_file.stem)
        pure_text = strip_markdown(text)
        char_count = len(pure_text.replace('\n', '').replace(' ', ''))
        thesis = extract_thesis(text)
        against = find_against_patterns(text)
        emotion = analyze_emotion(text)
        articles.append({
            'title': title, 'chars': char_count,
            'thesis_count': len(thesis), 'against_count': len(against),
            'against_top': against[:3], 'thesis_top': thesis[:5],
            'emotion': emotion, 'date': meta.get('publish_date', ''),
            'digest': meta.get('digest', ''),
        })
    total_chars = sum(a['chars'] for a in articles)
    avg_we = sum(a['emotion']['we_ratio'] for a in articles) / max(len(articles), 1)
    we_note = '(偏多「我」)' if avg_we < 0.3 else '(均衡)' if avg_we < 0.6 else '(偏多「我们」)'
    lines = ["# 乘百Pakco 公众号内容审计报告",
             f"\n> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"> 文章总数: {len(articles)} 篇 | 总字数: {total_chars:,}\n",
             "## 一、总览\n",
             "| 指标 | 数值 |", "|------|------|",
             f"| 文章总数 | {len(articles)} 篇 |",
             f"| 总字数 | {total_chars:,} 字 |",
             f"| 平均字数 | {total_chars//max(len(articles),1):,} 字/篇 |",
             f"| 我们/我 比例 | {avg_we:.2f} {we_note} |\n",
             "## 二、逐篇分析\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"### {i}. {a['title']}")
        lines.append(f"- 日期: {a.get('date', '未知')} | 字数: {a['chars']:,}")
        if a['against_top']:
            lines.append("\n**对抗句式**:")
            for p in a['against_top']:
                lines.append(f"> {p[:120]}")
        emo = a['emotion']
        lines.append(f"\n情绪: 正面{emo['positive']}/负面{emo['negative']}/我{emo['self_ref']}/我们{emo['we_ref']}(比{emo['we_ratio']:.2f})")
        lines.append("")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = '\n'.join(lines)
    OUTPUT_FILE.write_text(report, encoding='utf-8')
    print(f'[OK] 审计完成！扫描 {len(articles)} 篇文章')
    print(f'     报告: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
