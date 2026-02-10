"""arXiv数据源"""
import xml.etree.ElementTree as ET
import urllib.request
import ssl
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
        
        try:
            # arXiv API
            url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results=10"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url, headers={"User-Agent": "StellarPulse/1.0"})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                content = resp.read().decode('utf-8')
            
            # 解析Atom feed
            items = []
            root = ET.fromstring(content)
            
            # Atom命名空间
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                title = entry.findtext('atom:title', '', ns).strip()
                link = entry.find('atom:link', ns)
                link_url = link.get('href') if link is not None else ''
                summary = entry.findtext('atom:summary', '', ns).strip()
                published = entry.findtext('atom:published', '', ns)
                
                if title:
                    items.append({
                        "title": title[:200],
                        "link": link_url,
                        "summary": summary[:400] + "..." if len(summary) > 400 else summary,
                        "source": f"arXiv-{category}",
                        "pub_date": published,
                        "fetched_at": datetime.now().isoformat()
                    })
            
            return items
        except Exception as e:
            print(f"  [arXiv Error] {category}: {e}")
            return []
