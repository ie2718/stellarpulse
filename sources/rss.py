"""RSS数据源"""
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any
from urllib.request import urlopen, Request
import ssl
import re

try:
    from . import BaseSource
except ImportError:
    from __init__ import BaseSource

class RSSSource(BaseSource):
    """通用RSS源"""
    
    def fetch(self) -> List[Dict[str, Any]]:
        if not self.is_enabled():
            return []
        
        url = self.config.get("url")
        if not url:
            return []
        
        try:
            content = self._fetch_url(url)
            if not content:
                return []
            return self._parse_rss(content)
        except Exception as e:
            print(f"  [RSS Error] {self.name}: {e}")
            return []
    
    def _fetch_url(self, url: str, timeout: int = 15) -> str:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; StellarPulse/1.0)"})
        with urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    
    def _parse_rss(self, xml_content: str) -> List[Dict[str, Any]]:
        items = []
        try:
            # 移除CDATA标记以便解析
            xml_content = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', xml_content, flags=re.DOTALL)
            
            root = ET.fromstring(xml_content)
            channel = root.find('.//channel') or root
            
            for item in channel.findall('.//item'):
                title = self._get_text(item, 'title')
                link = self._get_text(item, 'link')
                desc = self._get_text(item, 'description')
                pub_date = self._get_text(item, 'pubDate')
                
                # 清理HTML标签
                desc = re.sub(r'<[^>]+>', '', desc)
                
                if title and link:
                    items.append({
                        "title": title[:200],
                        "link": link,
                        "summary": desc[:300] + "..." if len(desc) > 300 else desc,
                        "source": self.name,
                        "pub_date": pub_date,
                        "fetched_at": datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"  [Parse Error] {self.name}: {e}")
        
        return items
    
    def _get_text(self, element, tag: str) -> str:
        elem = element.find(tag)
        return elem.text.strip() if elem is not None and elem.text else ""
