"""关键词订阅管理系统"""
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

class SubscriptionManager:
    """管理用户关键词订阅"""
    
    def __init__(self, data_file: str = "/home/ec2-user/stellarpulse/keywords.json"):
        self.data_file = data_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"subscriptions": [], "alerts": []}
    
    def _save(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_subscription(self, keyword: str, categories: List[str] = None, 
                        notify: bool = True) -> Dict:
        """添加关键词订阅"""
        subscription = {
            "id": f"sub_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "keyword": keyword,
            "categories": categories or ["ai", "robotics", "space"],
            "notify": notify,
            "created_at": datetime.now().isoformat(),
            "match_count": 0
        }
        
        self.data["subscriptions"].append(subscription)
        self._save()
        return subscription
    
    def remove_subscription(self, sub_id: str) -> bool:
        """移除订阅"""
        original_len = len(self.data["subscriptions"])
        self.data["subscriptions"] = [
            s for s in self.data["subscriptions"] if s["id"] != sub_id
        ]
        if len(self.data["subscriptions"]) < original_len:
            self._save()
            return True
        return False
    
    def list_subscriptions(self) -> List[Dict]:
        """列出所有订阅"""
        return self.data.get("subscriptions", [])
    
    def check_matches(self, items: List[Dict]) -> List[Dict]:
        """检查内容是否匹配订阅"""
        matches = []
        subscriptions = self.data.get("subscriptions", [])
        
        for item in items:
            text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
            
            for sub in subscriptions:
                keyword = sub["keyword"].lower()
                
                # 支持简单通配符 * ?
                pattern = keyword.replace("*", ".*").replace("?", ".")
                if re.search(pattern, text):
                    match_info = {
                        "item": item,
                        "subscription": sub,
                        "matched_at": datetime.now().isoformat()
                    }
                    matches.append(match_info)
                    
                    # 更新匹配计数
                    sub["match_count"] = sub.get("match_count", 0) + 1
                    
                    # 记录告警
                    self.data["alerts"].append({
                        "subscription_id": sub["id"],
                        "keyword": sub["keyword"],
                        "title": item["title"],
                        "link": item["link"],
                        "time": datetime.now().isoformat()
                    })
        
        # 限制告警历史
        self.data["alerts"] = self.data["alerts"][-100:]
        self._save()
        
        return matches
    
    def get_recent_alerts(self, limit: int = 20) -> List[Dict]:
        """获取最近的告警"""
        alerts = self.data.get("alerts", [])
        return alerts[-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        subs = self.data.get("subscriptions", [])
        alerts = self.data.get("alerts", [])
        
        return {
            "subscription_count": len(subs),
            "total_alerts": len(alerts),
            "top_keywords": sorted(
                subs, 
                key=lambda x: x.get("match_count", 0), 
                reverse=True
            )[:5]
        }
