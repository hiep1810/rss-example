import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import feedparser
import csv
import time
import os

def _scrape_rss_links(url: str) -> List[str]:
    """
    Scrapes a webpage to find all RSS feed links.
    (Internal helper function)
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve RSS links page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rss_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".rss" in href or ".xml" in href:
            full_url = urljoin(url, href)
            rss_links.append(full_url)
    
    rss_links = list(set(rss_links))
    print(f"✅ Found {len(rss_links)} unique RSS links.")
    return rss_links

def _scrape_articles_from_feed(feed_url: str, csv_writer):
    """
    Parses an RSS feed and scrapes the content of each article.
    (Internal helper function)
    """
    print(f"--- Processing feed: {feed_url} ---")
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        print(f"📰 Scraping: {entry.title}")
        try:
            response = requests.get(entry.link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to retrieve article: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='article-content')

        if article_body:
            paragraphs = article_body.find_all('p')
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            csv_writer.writerow([entry.title, entry.link, entry.published, content])
        else:
            print(f"⚠️ Could not find article content for: {entry.link}")

def scrape_vietstock_articles() -> Dict[str, str]:
    """
    Main function to orchestrate the Vietstock article scraping process.
    Finds all RSS feeds and scrapes every article, saving them to a CSV file.

    Returns:
        A dictionary containing the path to the generated CSV file and a message.
    """
    start_time = time.time()
    base_url = "https://vietstock.vn/rss"
    rss_links = _scrape_rss_links(base_url)

    if not rss_links:
        return {"message": "No RSS links found. Scraping aborted.", "file_path": None}

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    csv_file = os.path.join(output_dir, f"vietstock_articles_{int(time.time())}.csv")
    csv_headers = ["Title", "Link", "Published", "Content"]

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        for link in rss_links:
            _scrape_articles_from_feed(link, writer)

    end_time = time.time()
    total_time = f"{end_time - start_time:.2f}"
    print(f"✅ All data has been successfully saved to {csv_file}")
    print(f"⏳ Total execution time: {total_time} seconds")
    return {
        "message": f"Scraping completed in {total_time} seconds.",
        "file_path": csv_file
    }
