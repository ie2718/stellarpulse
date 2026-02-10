"""
StellarPulse 交互式查询系统 - 简洁版 v2
修复: 数字回复与列表内容匹配
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

DATA_FILE = "/home/ec2-user/stellarpulse/data.json"
CACHE_FILE = "/tmp/stellarpulse_last_query.json"

def load_data() -> Dict:
    """加载数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"items": []}

def save_cache(items: List[Dict]):
    """保存最后查询结果"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False)
    except:
        pass

def load_cache() -> List[Dict]:
    """加载缓存的查询结果"""
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def format_time_ago(iso_time: str) -> str:
    """格式化相对时间"""
    try:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days}天前"
        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours}小时前"
        mins = diff.seconds // 60
        return f"{mins}分钟前" if mins > 0 else "刚刚"
    except:
        return ""

def search_items(items: List[Dict], query: str = None, category: str = None, limit: int = 8) -> List[Dict]:
    """搜索资讯"""
    results = items
    
    # 按分类筛选
    if category:
        results = [i for i in results if category in i.get('categories', [])]
    
    # 按关键词搜索
    if query:
        query_lower = query.lower()
        results = [i for i in results if query_lower in (i.get('title', '') + i.get('summary', '')).lower()]
    
    # 按时间排序
    results.sort(key=lambda x: x.get('fetched_at', ''), reverse=True)
    
    return results[:limit]

def format_list_item(item: Dict, index: int) -> str:
    """格式化列表项 - 简洁版"""
    title = item.get('title', '无标题')
    source = item.get('source', '')
    time_ago = format_time_ago(item.get('fetched_at', ''))
    
    # 分类emoji
    cats = item.get('categories', [])
    cat_emoji = ''
    if 'ai' in cats:
        cat_emoji = '🤖'
    elif 'robotics' in cats:
        cat_emoji = '🦾'
    elif 'space' in cats:
        cat_emoji = '🚀'
    
    # 重要性星星
    importance = item.get('importance', 0)
    stars = '⭐' * int(importance) if importance >= 2 else ''
    
    # 截断标题
    display_title = title[:40] + '...' if len(title) > 40 else title
    
    # 简洁格式
    meta = []
    if source:
        meta.append(source)
    if time_ago:
        meta.append(time_ago)
    
    meta_str = ' · '.join(meta) if meta else ''
    
    return f"{index}. {cat_emoji} {display_title} {stars}\n   {meta_str}".strip()

def format_detail(item: Dict) -> str:
    """格式化详情 - 简洁版"""
    title = item.get('title', '无标题')
    source = item.get('source', '')
    link = item.get('link', '')
    summary = item.get('ai_summary') or item.get('summary', '')
    time_ago = format_time_ago(item.get('fetched_at', ''))
    
    # 分类
    cats = item.get('categories', [])
    cat_labels = {
        'ai': '🤖 AI',
        'robotics': '🦾 机器人',
        'space': '🚀 航天'
    }
    cat_str = ' | '.join([cat_labels.get(c, c) for c in cats if c in cat_labels])
    
    lines = [f"📰 {title}"]
    
    if cat_str:
        lines.append(f"🏷️ {cat_str}")
    
    meta_parts = []
    if source:
        meta_parts.append(f"📡 {source}")
    if time_ago:
        meta_parts.append(time_ago)
    if meta_parts:
        lines.append(' · '.join(meta_parts))
    
    lines.append("")  # 空行
    
    if summary:
        # 清理摘要
        clean_summary = re.sub(r'\s+', ' ', summary).strip()
        if len(clean_summary) > 120:
            clean_summary = clean_summary[:117] + '...'
        lines.append(f"📝 {clean_summary}")
        lines.append("")
    
    if link:
        lines.append(f"🔗 {link}")
    
    return '\n'.join(lines)

def handle_command(command: str) -> str:
    """处理命令"""
    data = load_data()
    items = data.get('items', [])
    
    command = command.strip().lower()
    
    # 帮助
    if command in ['/help', 'help', '帮助']:
        return """📡 StellarPulse 命令

/ai     - AI & 大模型
/robot  - 机器人 & 具身智能  
/space  - 航天 & 太空
/hot    - 热门 TOP 5
/latest - 最新 5 条
/search 关键词 - 搜索
/help   - 显示帮助

💡 回复数字 1-8 查看详情"""
    
    # 最新
    if command in ['/latest', 'latest', '最新']:
        results = search_items(items, limit=5)
        save_cache(results)  # 保存到缓存
        if not results:
            return "📭 暂无数据"
        
        lines = ["📰 最新资讯\n"]
        for i, item in enumerate(results, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # 热门
    if command in ['/hot', 'hot', '热门']:
        hot_items = sorted(items, key=lambda x: x.get('importance', 0), reverse=True)[:5]
        save_cache(hot_items)  # 保存到缓存
        if not hot_items:
            return "📭 暂无数据"
        
        lines = ["🔥 热门资讯\n"]
        for i, item in enumerate(hot_items, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # AI
    if command in ['/ai', 'ai', '人工智能']:
        results = search_items(items, category='ai', limit=8)
        save_cache(results)  # 保存到缓存
        if not results:
            return "🤖 暂无 AI 相关资讯"
        
        lines = ["🤖 AI & 大模型\n"]
        for i, item in enumerate(results, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # 机器人
    if command in ['/robot', 'robot', 'robotics', '机器人', '具身智能']:
        results = search_items(items, category='robotics', limit=8)
        save_cache(results)  # 保存到缓存
        if not results:
            return "🦾 暂无机器人相关资讯"
        
        lines = ["🦾 具身智能 & 机器人\n"]
        for i, item in enumerate(results, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # 航天
    if command in ['/space', 'space', '航天', '太空']:
        results = search_items(items, category='space', limit=8)
        save_cache(results)  # 保存到缓存
        if not results:
            return "🚀 暂无航天相关资讯"
        
        lines = ["🚀 航天 & 太空\n"]
        for i, item in enumerate(results, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # 搜索
    if command.startswith('/search ') or command.startswith('搜索 '):
        query = command.split(' ', 1)[1] if ' ' in command else ''
        if not query:
            return "❓ 请输入关键词，如: /search GPT-5"
        
        results = search_items(items, query=query, limit=8)
        save_cache(results)  # 保存到缓存
        if not results:
            return f"🔍 未找到 '{query}' 相关内容"
        
        lines = [f"🔍 搜索: {query}\n"]
        for i, item in enumerate(results, 1):
            lines.append(format_list_item(item, i))
        lines.append("\n💡 回复数字查看详情")
        return '\n'.join(lines)
    
    # 默认
    results = search_items(items, limit=6)
    save_cache(results)  # 保存到缓存
    if not results:
        return "📭 暂无数据"
    
    lines = ["📡 科技情报\n"]
    for i, item in enumerate(results, 1):
        lines.append(format_list_item(item, i))
    lines.append("\n💡 回复数字查看详情 | /help 查看命令")
    return '\n'.join(lines)

def handle_number(number_str: str) -> str:
    """处理数字选择 - 从缓存读取"""
    try:
        num = int(number_str.strip())
        if num < 1 or num > 10:
            return "❌ 请输入 1-10 的数字"
        
        # 从缓存读取最后一次查询结果
        cached_items = load_cache()
        
        if not cached_items:
            return "❌ 请先发送查询命令 (如 /ai /robot)，再回复数字"
        
        if num > len(cached_items):
            return f"❌ 无效选择，当前列表只有 {len(cached_items)} 条"
        
        return format_detail(cached_items[num - 1])
        
    except ValueError:
        return "❌ 请输入有效数字"
    except Exception as e:
        return f"❌ 出错了: {str(e)}"

def should_respond(message: str) -> bool:
    """判断是否应该响应此消息"""
    commands = ['/tech', '/ai', '/robot', '/space', '/search', '/hot', '/latest', '/help',
                'ai', 'robot', 'space', 'tech', '热门', '最新', '帮助']
    
    msg_lower = message.strip().lower()
    
    # 命令匹配
    if any(msg_lower.startswith(cmd) for cmd in commands):
        return True
    
    # 数字回复
    if msg_lower in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        return True
    
    return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        print(handle_command(cmd))
