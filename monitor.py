#!/usr/bin/env python3
"""
StellarPulse / 星脉 - 科技情报监控系统 v2.0
功能：多源采集 + AI摘要 + 关键词订阅 + Web界面
"""

import json
import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# 添加sources目录到路径
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'sources'))

from rss import RSSSource
from hackernews import HackerNewsSource
from reddit import RedditSource
from arxiv import ArXivSource
from twitter import TwitterSource
from ai_summary import ContentAnalyzer
from subscription import SubscriptionManager

# ============ 配置 ============
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SITE_DATA_FILE = os.path.join(BASE_DIR, "docs/data/site_data.json")

def load_config() -> Dict:
    """加载配置"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_data() -> Dict:
    """加载数据"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"items": [], "last_run": None, "stats": {}}

def save_data(data: Dict):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============ 数据源采集 ============
def collect_all(config: Dict) -> List[Dict]:
    """采集所有数据源"""
    all_items = []
    sources_config = config.get("sources", {})
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始采集...")
    
    # RSS源
    for src_cfg in sources_config.get("rss", []):
        if src_cfg.get("enabled", True):
            print(f"  → RSS: {src_cfg['name']}...", end=" ")
            source = RSSSource(src_cfg)
            items = source.fetch()
            all_items.extend(items)
            print(f"✓ {len(items)}条")
    
    # API源
    for src_cfg in sources_config.get("api", []):
        if not src_cfg.get("enabled", True):
            continue
        
        source_type = src_cfg.get("type")
        print(f"  → API: {src_cfg['name']}...", end=" ")
        
        if source_type == "hn":
            source = HackerNewsSource(src_cfg)
        elif source_type == "reddit":
            source = RedditSource(src_cfg)
        elif source_type == "arxiv":
            source = ArXivSource(src_cfg)
        elif source_type == "twitter":
            source = TwitterSource(src_cfg)
        else:
            print("✗ 未知类型")
            continue
        
        items = source.fetch()
        all_items.extend(items)
        print(f"✓ {len(items)}条")
    
    print(f"  总计: {len(all_items)}条")
    return all_items

# ============ 内容处理 ============
def classify_content(title: str, summary: str, config: Dict) -> List[str]:
    """内容分类"""
    text = (title + " " + summary).lower()
    categories = []
    
    for cat, keywords in config.get("keywords", {}).items():
        for kw in keywords:
            if kw.lower() in text:
                categories.append(cat)
                break
    
    return categories if categories else ["other"]

def process_items(items: List[Dict], config: Dict) -> List[Dict]:
    """处理内容：去重、分类、AI分析"""
    print("\n[处理内容]")
    
    # 去重
    seen_links = set()
    unique_items = []
    for item in items:
        link = item.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_items.append(item)
    
    print(f"  去重后: {len(unique_items)}条")
    
    # 分类和分析
    analyzer = ContentAnalyzer()
    processed = []
    
    for item in unique_items:
        # 分类
        categories = classify_content(
            item.get("title", ""), 
            item.get("summary", ""), 
            config
        )
        item["categories"] = categories
        
        # 跳过无关内容
        if categories == ["other"]:
            continue
        
        # AI分析
        analysis = analyzer.analyze(
            item.get("title", ""),
            item.get("summary", "")
        )
        item["ai_summary"] = analysis["summary"]
        item["keywords"] = analysis["keywords"]
        item["importance"] = analysis["importance"]
        
        processed.append(item)
    
    print(f"  相关资讯: {len(processed)}条")
    
    # 按重要性排序
    processed.sort(key=lambda x: x.get("importance", 0), reverse=True)
    
    return processed

# ============ 报告生成 ============
def generate_report(items: List[Dict], config: Dict) -> tuple:
    """生成报告"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # 按分类组织
    by_cat = {"ai": [], "robotics": [], "space": []}
    for item in items:
        for cat in item.get("categories", []):
            if cat in by_cat:
                by_cat[cat].append(item)
    
    # 生成Markdown
    per_cat = config.get("settings", {}).get("items_per_category", 15)
    
    md = f"""# 📡 科技情报日报 | {date_str}

> 生成时间: {now.strftime("%H:%M")}  
> 本期精选: {len(items)} 条相关资讯 | AI自动摘要

---

## 📊 本期概览

| 领域 | 数量 | 热门关键词 |
|------|------|------------|
| 🤖 AI | {len(by_cat['ai'])} | {get_top_keywords(by_cat['ai'])} |
| 🦾 机器人 | {len(by_cat['robotics'])} | {get_top_keywords(by_cat['robotics'])} |
| 🚀 航天 | {len(by_cat['space'])} | {get_top_keywords(by_cat['space'])} |

---

## 🤖 AI & 大模型 ({len(by_cat['ai'])} 条)

"""
    
    for item in by_cat["ai"][:per_cat]:
        md += format_item(item)
    
    md += f"""
## 🦾 具身智能 & 机器人 ({len(by_cat['robotics'])} 条)

"""
    for item in by_cat["robotics"][:per_cat]:
        md += format_item(item)
    
    md += f"""
## 🚀 航天 & 太空 ({len(by_cat['space'])} 条)

"""
    for item in by_cat["space"][:per_cat]:
        md += format_item(item)
    
    md += """
---

*本报告由 StellarPulse 自动生成*  
*Web界面: http://your-server:8080*
"""
    
    # 保存
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = f"{REPORTS_DIR}/report-{date_str}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    # 生成网站数据
    generate_site_data(items, by_cat, config)
    
    return report_path, md


def generate_site_data(items: List[Dict], by_cat: Dict, config: Dict):
    """生成 GitHub Pages 网站数据"""
    now = datetime.now()
    
    # 统计数据源
    sources = {}
    for item in items:
        src = item.get("source", "Unknown")
        sources[src] = sources.get(src, 0) + 1
    
    # 构建网站数据
    site_data = {
        "site": {
            "name": "StellarPulse",
            "name_cn": "星脉",
            "tagline": "Pulse from the stars, capturing every ripple of tech frontier.",
            "tagline_cn": "来自星辰的脉动，捕捉科技前沿每一丝波动。",
            "version": "2.0",
            "last_update": now.isoformat(),
            "total_items": len(items)
        },
        "categories": {
            "ai": {
                "name": "AI & LLM",
                "name_cn": "AI & 大模型",
                "emoji": "🤖",
                "count": len(by_cat.get("ai", []))
            },
            "robotics": {
                "name": "Robotics",
                "name_cn": "具身智能",
                "emoji": "🦾",
                "count": len(by_cat.get("robotics", []))
            },
            "space": {
                "name": "Space",
                "name_cn": "航天",
                "emoji": "🚀",
                "count": len(by_cat.get("space", []))
            }
        },
        "stats": {
            "total_items": len(items),
            "today_items": len(items),
            "sources": sources,
            "last_update": now.isoformat()
        },
        "trending": sorted(items, key=lambda x: x.get("importance", 0), reverse=True)[:10],
        "latest": sorted(items, key=lambda x: x.get("fetched_at", ""), reverse=True)[:20],
        "updated_at": now.isoformat()
    }
    
    # 保存网站数据
    os.makedirs(os.path.dirname(SITE_DATA_FILE), exist_ok=True)
    with open(SITE_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(site_data, f, ensure_ascii=False, indent=2)
    
    print(f"  网站数据已更新: {SITE_DATA_FILE}")

def format_item(item: Dict) -> str:
    """格式化单条资讯"""
    importance = item.get("importance", 0)
    stars = "⭐" * int(importance)
    
    md = f"""### {item['title']} {stars}

- 🔗 [{item['link'][:60]}...]({item['link']})
- 📡 {item['source']} | 🕐 {item.get('fetched_at', '')[:16]}
"""
    
    if item.get("ai_summary"):
        md += f"- 📝 AI摘要: {item['ai_summary']}\n"
    
    if item.get("keywords"):
        md += f"- 🏷️ 关键词: {', '.join(item['keywords'][:5])}\n"
    
    md += "\n"
    return md

def get_top_keywords(items: List[Dict]) -> str:
    """获取热门关键词"""
    all_keywords = []
    for item in items[:5]:
        all_keywords.extend(item.get("keywords", []))
    
    # 统计频率
    freq = {}
    for kw in all_keywords:
        freq[kw] = freq.get(kw, 0) + 1
    
    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
    return ', '.join([k[0] for k in top]) if top else 'N/A'

# ============ 关键词订阅检查 ============
def check_subscriptions(items: List[Dict]) -> List[Dict]:
    """检查关键词匹配"""
    mgr = SubscriptionManager()
    matches = mgr.check_matches(items)
    
    if matches:
        print(f"\n[关键词订阅] 发现 {len(matches)} 条匹配")
        for m in matches[:5]:
            print(f"  🔔 {m['subscription']['keyword']}: {m['item']['title'][:50]}...")
    
    return matches

# ============ WhatsApp摘要 ============
def generate_whatsapp_summary(items: List[Dict], matches: List[Dict]) -> str:
    """生成WhatsApp推送摘要"""
    now = datetime.now().strftime("%m-%d %H:%M")
    
    # 统计
    counts = {"ai": 0, "robotics": 0, "space": 0}
    for item in items:
        for cat in item.get("categories", []):
            if cat in counts:
                counts[cat] += 1
    
    # 取Top 3标题
    top_items = items[:3]
    
    msg = f"""📡 StellarPulse 日报 {now}

🤖 AI: {counts['ai']} | 🦾 机器人: {counts['robotics']} | 🚀 航天: {counts['space']}

🔥 热门资讯:
"""
    for i, item in enumerate(top_items, 1):
        title = item['title'][:35] + "..." if len(item['title']) > 35 else item['title']
        msg += f"{i}. {title}\n"
    
    if matches:
        msg += f"\n🔔 关键词命中: {len(matches)}条\n"
    
    msg += "\n📄 完整报告已生成\n🌐 Web: http://your-server:8080"
    
    return msg

def sync_to_github():
    """同步到 GitHub（仅在内容有变更时提交）"""
    try:
        # 检查是否有变更
        subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
        # 检查暂存区是否有变更
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BASE_DIR, capture_output=True)
        if result.returncode != 0:  # 有变更才提交
            commit_msg = f"chore: auto-update StellarPulse data {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
            print("\n[GitHub] 已自动同步提交")
        else:
            print("\n[GitHub] 无内容变更，跳过提交")
    except subprocess.CalledProcessError as e:
        print(f"\n[GitHub] 自动同步失败: {e}")

# ============ 主流程 ============
def main():
    parser = argparse.ArgumentParser(description='StellarPulse')
    parser.add_argument('--web', action='store_true', help='启动Web服务器')
    parser.add_argument('--subscribe', type=str, help='添加关键词订阅')
    parser.add_argument('--list-subs', action='store_true', help='列出订阅')
    args = parser.parse_args()
    
    # Web服务器模式
    if args.web:
        from web.server import start_server
        config = load_config()
        port = config.get("settings", {}).get("web_port", 8080)
        start_server(port)
        return
    
    # 订阅管理
    if args.subscribe:
        mgr = SubscriptionManager()
        sub = mgr.add_subscription(args.subscribe)
        print(f"✅ 已添加订阅: {args.subscribe} (ID: {sub['id']})")
        return
    
    if args.list_subs:
        mgr = SubscriptionManager()
        subs = mgr.list_subscriptions()
        print(f"🔔 当前订阅 ({len(subs)}个):")
        for s in subs:
            print(f"  • {s['keyword']} (匹配: {s.get('match_count', 0)}次)")
        return
    
    # 正常采集模式
    print("=" * 60)
    print("📡 StellarPulse v2.0 启动")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    data = load_data()
    
    # 1. 采集
    raw_items = collect_all(config)
    
    # 2. 处理
    processed = process_items(raw_items, config)
    
    # 3. 去重 (与历史数据)
    existing_links = {item["link"] for item in data.get("items", [])}
    new_items = [item for item in processed if item["link"] not in existing_links]
    print(f"\n[数据更新] 新增: {len(new_items)}条")
    
    # 4. 保存
    data["items"] = (data.get("items", []) + new_items)[-1000:]  # 保留1000条
    data["last_run"] = datetime.now().isoformat()
    data["stats"] = {
        "total_items": len(data["items"]),
        "last_new_items": len(new_items),
        "last_run": datetime.now().isoformat()
    }
    save_data(data)
    
    # 5. 检查订阅
    matches = check_subscriptions(new_items)
    
    # 6. 生成报告
    if processed:
        report_path, full_report = generate_report(processed, config)
        print(f"\n[报告生成] {report_path}")
        
        # 7. WhatsApp摘要
        whatsapp_msg = generate_whatsapp_summary(processed, matches)
        print("\n" + "=" * 60)
        print("WHATSAPP_MSG_START")
        print(whatsapp_msg)
        print("WHATSAPP_MSG_END")
    else:
        print("\n[报告] 本期无相关资讯")
    
    # 自动同步到 GitHub
    sync_to_github()
    
    print("=" * 60)
    print("✅ 完成")

if __name__ == "__main__":
    main()
