"""Web管理界面"""
import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading

# 页面模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StellarPulse - 星脉 | 科技情报监控</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            line-height: 1.6;
        }
        .header { 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #0f3460;
        }
        .header h1 { color: #e94560; margin-bottom: 10px; }
        .nav { 
            display: flex; 
            justify-content: center; 
            gap: 20px; 
            padding: 15px;
            background: #0f0f0f;
        }
        .nav a { 
            color: #e94560; 
            text-decoration: none; 
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav a:hover { background: #1a1a2e; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card { 
            background: #1a1a2e; 
            padding: 20px; 
            border-radius: 10px;
            text-align: center;
            border: 1px solid #0f3460;
        }
        .stat-card h3 { color: #e94560; font-size: 2em; }
        .stat-card p { color: #888; margin-top: 5px; }
        .section { 
            background: #1a1a2e; 
            padding: 20px; 
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #0f3460;
        }
        .section h2 { color: #e94560; margin-bottom: 15px; }
        .news-item { 
            padding: 15px; 
            border-bottom: 1px solid #0f3460;
            transition: background 0.2s;
        }
        .news-item:hover { background: #16213e; }
        .news-item:last-child { border-bottom: none; }
        .news-title { 
            font-size: 1.1em; 
            color: #fff;
            margin-bottom: 8px;
        }
        .news-title a { color: #4fbdba; text-decoration: none; }
        .news-title a:hover { text-decoration: underline; }
        .news-meta { 
            font-size: 0.85em; 
            color: #888;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .tag { 
            background: #0f3460; 
            padding: 2px 8px; 
            border-radius: 4px;
            font-size: 0.8em;
        }
        .tag.ai { background: #e94560; }
        .tag.robotics { background: #4fbdba; }
        .tag.space { background: #533483; }
        .btn {
            background: #e94560;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
        }
        .btn:hover { background: #ff6b6b; }
        input[type="text"] {
            background: #0f0f0f;
            border: 1px solid #0f3460;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 5px;
            width: 300px;
        }
        .subscription-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .sub-item {
            background: #0f3460;
            padding: 8px 15px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .sub-item .remove {
            color: #e94560;
            cursor: pointer;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .nav { flex-direction: column; align-items: center; }
            input[type="text"] { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📡 StellarPulse / 星脉</h1>
        <p>AI · 机器人 · 航天 科技情报监控</p>
    </div>
    <nav class="nav">
        <a href="/">📰 最新资讯</a>
        <a href="/?page=subscriptions">🔔 订阅管理</a>
        <a href="/?page=stats">📊 数据统计</a>
        <a href="/?page=reports">📄 历史报告</a>
    </nav>
    <div class="container">
        {{content}}
    </div>
</body>
</html>
'''

class StellarPulseHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        page = params.get('page', [''])[0]
        
        if page == 'subscriptions':
            content = self._render_subscriptions()
        elif page == 'stats':
            content = self._render_stats()
        elif page == 'reports':
            content = self._render_reports()
        else:
            content = self._render_home()
        
        html = HTML_TEMPLATE.replace('{{content}}', content)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        if parsed.path == '/api/subscribe':
            keyword = params.get('keyword', [''])[0]
            if keyword:
                self._add_subscription(keyword)
            self.send_response(302)
            self.send_header('Location', '/?page=subscriptions')
            self.end_headers()
        elif parsed.path == '/api/unsubscribe':
            sub_id = params.get('id', [''])[0]
            if sub_id:
                self._remove_subscription(sub_id)
            self.send_response(302)
            self.send_header('Location', '/?page=subscriptions')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _render_home(self) -> str:
        """渲染首页 - 最新资讯"""
        # 加载数据
        items = self._load_items()
        
        # 统计
        ai_count = sum(1 for i in items if 'ai' in i.get('categories', []))
        robotics_count = sum(1 for i in items if 'robotics' in i.get('categories', []))
        space_count = sum(1 for i in items if 'space' in i.get('categories', []))
        
        html = f'''
        <div class="stats">
            <div class="stat-card">
                <h3>{len(items)}</h3>
                <p>📊 总资讯数</p>
            </div>
            <div class="stat-card">
                <h3>{ai_count}</h3>
                <p>🤖 AI & 大模型</p>
            </div>
            <div class="stat-card">
                <h3>{robotics_count}</h3>
                <p>🦾 具身智能</p>
            </div>
            <div class="stat-card">
                <h3>{space_count}</h3>
                <p>🚀 航天</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📰 最新资讯</h2>
        '''
        
        for item in items[:20]:
            cats = item.get('categories', ['other'])
            cat_tags = ''.join([f'<span class="tag {c}">{c.upper()}</span>' for c in cats if c != 'other'])
            
            html += f'''
            <div class="news-item">
                <div class="news-title">
                    <a href="{item.get('link', '#')}" target="_blank">{item.get('title', 'Untitled')}</a>
                </div>
                <div class="news-meta">
                    <span>📡 {item.get('source', 'Unknown')}</span>
                    <span>🕐 {item.get('fetched_at', '')[:16]}</span>
                    {cat_tags}
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _render_subscriptions(self) -> str:
        """渲染订阅管理页"""
        subs = self._load_subscriptions()
        
        html = '''
        <div class="section">
            <h2>🔔 关键词订阅</h2>
            <p>添加关键词，当相关内容出现时立即通知</p>
            <form action="/api/subscribe" method="POST" style="margin-top: 15px;">
                <input type="text" name="keyword" placeholder="输入关键词，如: GPT-5, 宇树, SpaceX..." required>
                <button type="submit" class="btn">添加订阅</button>
            </form>
            
            <div class="subscription-list">
        '''
        
        for sub in subs:
            html += f'''
            <div class="sub-item">
                {sub.get('keyword', '')}
                <form action="/api/unsubscribe" method="POST" style="display:inline;">
                    <input type="hidden" name="id" value="{sub.get('id', '')}">
                    <button type="submit" class="remove" style="background:none;border:none;">×</button>
                </form>
            </div>
            '''
        
        html += '</div></div>'
        return html
    
    def _render_stats(self) -> str:
        """渲染统计页"""
        items = self._load_items()
        subs = self._load_subscriptions()
        
        # 计算统计数据
        sources = {}
        categories = {'ai': 0, 'robotics': 0, 'space': 0}
        
        for item in items:
            src = item.get('source', 'Unknown')
            sources[src] = sources.get(src, 0) + 1
            
            for cat in item.get('categories', []):
                if cat in categories:
                    categories[cat] += 1
        
        html = '''
        <div class="section">
            <h2>📊 数据统计</h2>
            <h3 style="margin-top: 20px; color: #4fbdba;">📡 数据源分布</h3>
        '''
        
        for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            html += f'<p>{src}: {count} 条</p>'
        
        html += '<h3 style="margin-top: 20px; color: #4fbdba;">🏷️ 分类统计</h3>'
        html += f'<p>🤖 AI: {categories["ai"]} 条</p>'
        html += f'<p>🦾 Robotics: {categories["robotics"]} 条</p>'
        html += f'<p>🚀 Space: {categories["space"]} 条</p>'
        html += f'<p>🔔 订阅数: {len(subs)} 个</p>'
        
        html += '</div>'
        return html
    
    def _render_reports(self) -> str:
        """渲染历史报告页"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(base_dir, "reports")
        reports = []
        
        if os.path.exists(reports_dir):
            for f in sorted(os.listdir(reports_dir), reverse=True):
                if f.endswith('.md'):
                    reports.append(f)
        
        html = '''
        <div class="section">
            <h2>📄 历史报告</h2>
        '''
        
        for report in reports[:30]:
            date = report.replace('report-', '').replace('.md', '')
            html += f'''
            <div class="news-item">
                <div class="news-title">
                    <a href="/reports/{report}" target="_blank">📅 {date} 日报</a>
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _load_items(self) -> list:
        """加载数据"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(os.path.join(base_dir, 'data.json'), 'r') as f:
                data = json.load(f)
                return data.get('items', [])
        except:
            return []
    
    def _load_subscriptions(self) -> list:
        """加载订阅"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(os.path.join(base_dir, 'keywords.json'), 'r') as f:
                data = json.load(f)
                return data.get('subscriptions', [])
        except:
            return []
    
    def _add_subscription(self, keyword: str):
        """添加订阅"""
        from subscription import SubscriptionManager
        mgr = SubscriptionManager()
        mgr.add_subscription(keyword)
    
    def _remove_subscription(self, sub_id: str):
        """移除订阅"""
        from subscription import SubscriptionManager
        mgr = SubscriptionManager()
        mgr.remove_subscription(sub_id)
    
    def log_message(self, format, *args):
        pass  # 静默日志


def start_server(port: int = 8080):
    """启动Web服务器"""
    server = HTTPServer(('0.0.0.0', port), StellarPulseHandler)
    print(f"🌐 Web界面启动: http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == '__main__':
    start_server()
