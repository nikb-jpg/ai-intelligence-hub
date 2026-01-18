import feedparser
import json
import os
from datetime import datetime

# 1. Define our 3-Section Sources
FEEDS = {
    "Research": "https://arxiv.org/rss/cs.AI",
    "Practitioner": "https://hnrss.org/newest?q=AI+OR+Machine+Learning",
    "Prompting": "https://www.maginative.com/rss/"
}

def fetch_data():
    all_data = {}
    today_str = datetime.now().strftime("%Y-%m-%d")
    markdown_content = f"# AI Intelligence Briefing - {today_str}\n\n"

    for section, url in FEEDS.items():
        print(f"Fetching {section}...")
        feed = feedparser.parse(url)
        # Get the top 5 entries for each section
        entries = feed.entries[:5]
        
        all_data[section] = []
        markdown_content += f"## {section}\n"
        
        for entry in entries:
            # Simple cleaning of summary text
            summary = entry.get("summary", "No summary available.")
            if "<" in summary: # Basic HTML tag removal
                summary = summary.split(">")[-1]
            summary = summary[:200] + "..."

            item = {
                "title": entry.title,
                "link": entry.link,
                "summary": summary
            }
            all_data[section].append(item)
            markdown_content += f"- **[{item['title']}]({item['link']})**\n  _{item['summary']}_\n\n"

    # 2. Save Daily Markdown for NotebookLM
    if not os.path.exists('daily_logs'):
        os.makedirs('daily_logs')
    
    with open(f"daily_logs/{today_str}.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # 3. Update Master Archive (JSON)
    archive_file = 'archive.json'
    if os.path.exists(archive_file):
        try:
            with open(archive_file, 'r') as f:
                full_archive = json.load(f)
        except:
            full_archive = {}
    else:
        full_archive = {}

    full_archive[today_str] = all_data

    with open(archive_file, 'w', encoding="utf-8") as f:
        json.dump(full_archive, f, indent=4)

    print(f"Successfully archived news for {today_str}")

if __name__ == "__main__":
    fetch_data()
