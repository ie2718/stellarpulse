"""arXiv数据源 - 使用feedparser增强"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Any

try:
    from . import BaseSource
except ImportError:
    from __init__ import BaseSource

class ArXivSource(BaseSource):
    """arXiv论文源"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        category = self.config.get("category", "cs.AI")
        max_results = self.config.get("max_results", 10)
        
        try:
            # arXiv API
            url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            # 使用feedparser解析Atom feed
            feed = feedparser.parse(response.content)
            
            items = []
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                summary = entry.get("summary", "").strip()
                published = entry.get("published", "")
                
                if title:
                    items.append({
                        "title": title[:200],
                        "link": link,
                        "summary": summary[:400] + "..." if len(summary) > 400 else summary,
                        "source": f"arXiv-{category}",
                        "pub_date": published,
                        "fetched_at": datetime.now().isoformat()
                    })
            
            return items
        except Exception as e:
            print(f"  [arXiv Error] {category}: {e}")
            return []
