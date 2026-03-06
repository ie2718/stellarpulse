import json
import os
from datetime import datetime

# Paths
TD_MERGED = "/tmp/td-merged.json"
SP_BASE = "/Users/yujie/.openclaw/workspace/stellarpulse"
SP_DATA = os.path.join(SP_BASE, "data.json")

def sync():
    if not os.path.exists(TD_MERGED):
        print(f"Error: {TD_MERGED} not found.")
        return

    with open(TD_MERGED, 'r') as f:
        td_data = json.load(f)

    if not os.path.exists(SP_DATA):
        sp_data = {"items": [], "last_run": None, "stats": {}}
    else:
        with open(SP_DATA, 'r') as f:
            sp_data = json.load(f)

    existing_links = {item['link'] for item in sp_data['items']}
    new_items = []

    # Mapping topics
    topic_map = {
        "llm": "ai",
        "ai-agent": "ai",
        "frontier-tech": "ai", # Default to AI for tech news in SP
        "crypto": "other"
    }

    for topic_id, topic_content in td_data.get('topics', {}).items():
        sp_cat = topic_map.get(topic_id, "other")
        
        for art in topic_content.get('articles', []):
            link = art.get('link')
            if link and link not in existing_links:
                item = {
                    "title": art.get('title'),
                    "link": link,
                    "summary": art.get('snippet') or art.get('title'),
                    "source": art.get('source_name') or art.get('source_type') or "Unknown",
                    "pub_date": art.get('date'),
                    "fetched_at": datetime.now().isoformat(),
                    "categories": [sp_cat],
                    "ai_summary": art.get('snippet'),
                    "keywords": art.get('topics', []),
                    "importance": float(art.get('quality_score', 1)) / 2.0 # Normalize score
                }
                new_items.append(item)
                existing_links.add(link)

    # Prepend new items
    sp_data['items'] = (new_items + sp_data['items'])[:1000]
    sp_data['last_run'] = datetime.now().isoformat()
    
    with open(SP_DATA, 'w') as f:
        json.dump(sp_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully synced {len(new_items)} items from tech-news-digest to StellarPulse.")

if __name__ == "__main__":
    sync()
