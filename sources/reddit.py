"""Reddit数据源"""
import json
import urllib.request
import ssl
from datetime import datetime
from typing import List, Dict, Any

try:
    from . import BaseSource
except ImportError:
    from __init__ import BaseSource

class RedditSource(BaseSource):
    """Reddit子版块数据源"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        subreddit = self.config.get("subreddit", "technology")
        
        try:
            # Reddit JSON API (无需认证)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=15"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                url, 
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            
            items = []
            for post in data.get('data', {}).get('children', []):
                p = post.get('data', {})
                if p.get('title'):
                    items.append({
                        "title": p['title'][:200],
                        "link": f"https://reddit.com{p.get('permalink', '')}",
                        "summary": f"👍 {p.get('score', 0)} | 💬 {p.get('num_comments', 0)} | r/{subreddit}",
                        "source": f"Reddit-r/{subreddit}",
                        "pub_date": datetime.fromtimestamp(p.get('created_utc', 0)).isoformat() if p.get('created_utc') else '',
                        "fetched_at": datetime.now().isoformat()
                    })
            
            return items
        except Exception as e:
            print(f"  [Reddit Error] r/{subreddit}: {e}")
            return []
