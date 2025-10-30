#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, datetime, feedparser, html, re
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data", "feeds.json")
TEMPLATES = os.path.join(ROOT, "templates")
DOCS = os.path.join(ROOT, "docs")
NEWS_DIR = os.path.join(DOCS, "news")
os.makedirs(NEWS_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
index_tpl = env.get_template("index.html.j2")
daily_tpl = env.get_template("daily.html.j2")

def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()

def summarize(text, limit=150):
    text = strip_html(text)
    if len(text) > limit:
        return text[:limit].rsplit(" ", 1)[0] + "..."
    return text

def load_feeds():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)["feeds"]

def fetch_news():
    items = []
    for url in load_feeds():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                title = entry.get("title", "No title")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description","") or ""
                date = entry.get("published", "") or entry.get("updated", "")
                items.append({
                    "title": strip_html(title),
                    "link": link,
                    "summary": summarize(summary),
                    "source": feed.feed.get("title", ""),
                    "date": date
                })
        except Exception as e:
            print("Error on feed:", url, e)
    return sorted(items, key=lambda x: x["date"], reverse=True)

def main():
    now_jst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    today = now_jst.date().isoformat()
    items = fetch_news()
    if not items:
        print("No news fetched.")
        return

    daily_path = os.path.join(NEWS_DIR, f"{today}.html")
    with open(daily_path, "w", encoding="utf-8") as f:
        f.write(daily_tpl.render(date=today, items=items))

    all_days = sorted(
        [f.replace(".html", "") for f in os.listdir(NEWS_DIR) if f.endswith(".html")],
        reverse=True
    )
    latest = all_days[:10]

    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_tpl.render(days=latest, today=today))

    print(f"Generated {len(items)} items for {today}")

if __name__ == "__main__":
    main()
