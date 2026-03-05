"""RSS数据源 - 使用feedparser增强鲁棒性"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup

try:
    from . import BaseSource
except ImportError:
    from __init__ import BaseSource

class RSSSource(BaseSource):
    """使用feedparser的RSS源"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        url = self.config.get("url")
        if not url:
            return []
        
        try:
            # 使用requests获取内容，带上User-Agent
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 使用feedparser解析
            feed = feedparser.parse(response.content)
            
            items = []
            for entry in feed.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                
                # 获取摘要
                summary = ""
                if "summary" in entry:
                    summary = entry.summary
                elif "description" in entry:
                    summary = entry.description
                elif "content" in entry:
                    summary = entry.content[0].value
                
                # 清理HTML
                if summary:
                    summary = BeautifulSoup(summary, "html.parser").get_text()
                    summary = re.sub(r'\s+', ' ', summary).strip()
                
                pub_date = entry.get("published", "")
                
                if title and link:
                    items.append({
                        "title": title[:200],
                        "link": link,
                        "summary": summary[:300] + "..." if len(summary) > 300 else summary,
                        "source": self.name,
                        "pub_date": pub_date,
                        "fetched_at": datetime.now().isoformat()
                    })
            
            return items
            
        except Exception as e:
            print(f"  [RSS Error] {self.name}: {e}")
            return []
