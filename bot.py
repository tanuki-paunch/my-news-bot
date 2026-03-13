import feedparser
from bs4 import BeautifulSoup
import datetime
import os

# --- CONFIGURATION ---
KEYWORDS = ["AI", "Space", "Technology"] # Add your own here!
RSS_FEEDS = [
    "https://news.google.com/rss",
    "https://www.theverge.com/rss/index.xml"
]

def fetch_news():
    results = []
    found_any = False
    
    print(f"Starting search at {datetime.datetime.now()}")
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title
                # Simple keyword check
                if any(key.lower() in title.lower() for key in KEYWORDS):
                    found_any = True
                    # Get summary or a fallback string
                    summary_raw = getattr(entry, 'summary', 'No summary provided.')
                    summary_clean = BeautifulSoup(summary_raw, "html.parser").get_text()[:200] + "..."
                    
                    results.append(f"""
                    <div style='margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 15px;'>
                        <h3 style='margin-bottom: 5px;'><a href='{entry.link}' target='_blank' style='color: #1a73e8; text-decoration: none;'>{title}</a></h3>
                        <p style='color: #3c4043; line-height: 1.5;'>{summary_clean}</p>
                        <small style='color: #70757a;'>Source: {url.split('/')[2]} | {datetime.datetime.now().strftime('%b %d, %Y')}</small>
                    </div>
                    """)
        except Exception as e:
            print(f"Error scanning {url}: {e}")

    if not found_any:
        return "<h2>No news found for your keywords today.</h2><p>Try adding broader keywords to bot.py!</p>"
    
    return "".join(results)

# Generate HTML
news_html = fetch_news()
full_page = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My News Bot</title>
</head>
<body style='font-family: -apple-system, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #202124;'>
    <header style='border-bottom: 2px solid #1a73e8; margin-bottom: 30px;'>
        <h1 style='color: #1a73e8; margin-bottom: 10px;'>Personal News Briefing</h1>
        <p style='color: #70757a;'>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
    </header>
    <main>
        {news_html}
    </main>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_page)
print("Successfully updated index.html")