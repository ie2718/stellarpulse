"""
X (Twitter) 数据源
需要 Bearer Token (来自 X Developer Portal)
"""
import json
import urllib.request
import ssl
from datetime import datetime
from typing import List, Dict, Any

from sources import BaseSource

class TwitterSource(BaseSource):
    """X/Twitter API v2 数据源"""
    
    BASE_URL = "https://api.twitter.com/2"
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        bearer_token = self.config.get("bearer_token")
        query = self.config.get("query", "AI OR \"artificial intelligence\" -is:retweet")
        max_results = self.config.get("max_results", 10)
        
        if not bearer_token:
            print(f"  [X/Twitter Error] {self.name}: Missing bearer_token")
            return []
        
        try:
            # 搜索最近推文
            url = f"{self.BASE_URL}/tweets/search/recent"
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "tweet.fields": "created_at,public_metrics,author_id",
                "expansions": "author_id",
                "user.fields": "username,name"
            }
            
            # 构建查询字符串
            query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
            full_url = f"{url}?{query_string}"
            
            # 请求头
            headers = {
                "Authorization": f"Bearer {bearer_token}",
                "User-Agent": "StellarPulse/1.0"
            }
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            
            # 解析推文
            items = []
            tweets = data.get('data', [])
            users = {u['id']: u for u in data.get('includes', {}).get('users', [])}
            
            for tweet in tweets:
                author_id = tweet.get('author_id')
                author = users.get(author_id, {})
                username = author.get('username', 'unknown')
                display_name = author.get('name', username)
                
                metrics = tweet.get('public_metrics', {})
                
                items.append({
                    "title": tweet.get('text', '')[:100] + "..." if len(tweet.get('text', '')) > 100 else tweet.get('text', ''),
                    "link": f"https://twitter.com/{username}/status/{tweet.get('id')}",
                    "summary": f"❤️ {metrics.get('like_count', 0)} | 🔁 {metrics.get('retweet_count', 0)} | 💬 {metrics.get('reply_count', 0)} | by @{username}",
                    "source": f"X/@{username}",
                    "pub_date": tweet.get('created_at', ''),
                    "fetched_at": datetime.now().isoformat(),
                    "raw_text": tweet.get('text', '')
                })
            
            return items
            
        except Exception as e:
            print(f"  [X/Twitter Error] {self.name}: {e}")
            return []


class TwitterSourceSimple(BaseSource):
    """简化版 X/Twitter 数据源 (无需API，使用Nitter等镜像)"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        """
        简化实现：通过 Nitter 或其他镜像获取公开推文
        不需要 API Key，但稳定性较低
        """
        if not self.is_enabled():
            return []
        
        # 获取配置的搜索词或用户名列表
        queries = self.config.get("queries", ["AI", "OpenAI", "SpaceX"])
        nitter_instance = self.config.get("nitter_instance", "https://nitter.net")
        
        items = []
        
        for query in queries[:3]:  # 限制查询数量
            try:
                url = f"{nitter_instance}/search?f=tweets&q={urllib.parse.quote(query)}"
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                
                with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                    html = resp.read().decode('utf-8')
                
                # 简单解析 (Nitter HTML结构)
                # 注意：这依赖于Nitter的具体实现，可能不稳定
                items.extend(self._parse_nitter_html(html, query))
                
            except Exception as e:
                print(f"  [Nitter Error] {query}: {e}")
        
        return items[:10]  # 限制返回数量
    
    def _parse_nitter_html(self, html: str, query: str) -> List[Dict]:
        """解析 Nitter HTML"""
        import re
        items = []
        
        # 简单正则匹配推文
        # 格式: tweet-content 中的文本
        tweet_pattern = r'<div class="tweet-content"[^>]*>.*?(<div class="tweet-body"[^>]*>.*?)</div>'
        tweets = re.findall(tweet_pattern, html, re.DOTALL)
        
        for tweet_html in tweets[:5]:
            try:
                # 提取用户名
                user_match = re.search(r'href="/([^"]+)"', tweet_html)
                username = user_match.group(1) if user_match else 'unknown'
                
                # 提取推文内容
                text_match = re.search(r'<div class="tweet-content media-body"[^>]*>(.*?)</div>', tweet_html, re.DOTALL)
                if text_match:
                    text = re.sub(r'<[^>]+>', '', text_match.group(1))
                    text = text.strip()[:200]
                    
                    items.append({
                        "title": text[:100] + "..." if len(text) > 100 else text,
                        "link": f"https://twitter.com/{username}",
                        "summary": f"Search: {query}",
                        "source": f"X/@{username}",
                        "pub_date": "",
                        "fetched_at": datetime.now().isoformat()
                    })
            except:
                continue
        
        return items
