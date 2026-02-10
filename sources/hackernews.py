"""HackerNews数据源"""
import json
from datetime import datetime
from typing import List, Dict, Any
from urllib.request import urlopen, Request
import ssl

try:
    from . import BaseSource
except ImportError:
    from __init__ import BaseSource

class HackerNewsSource(BaseSource):
    """HackerNews热门故事"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        try:
            # 获取热门故事ID
            top_ids = self._fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
            if not top_ids:
                return []
            
            items = []
            for story_id in top_ids[:20]:  # 前20条
                story = self._fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                if story and story.get('title'):
                    items.append({
                        "title": story['title'],
                        "link": story.get('url') or f"https://news.ycombinator.com/item?id={story_id}",
                        "summary": f"👍 {story.get('score', 0)} | 💬 {story.get('descendants', 0)}",
                        "source": "HackerNews",
                        "pub_date": datetime.fromtimestamp(story.get('time', 0)).isoformat() if story.get('time') else '',
                        "fetched_at": datetime.now().isoformat()
                    })
            return items
        except Exception as e:
            print(f"  [HN Error] {e}")
            return []
    
    def _fetch_json(self, url: str) -> Any:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15, context=ctx) as resp:
            return json.loads(resp.read().decode('utf-8'))
