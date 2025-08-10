import feedparser
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time

def scrape_rss_links(url):
    """
    Scrapes a webpage to find all RSS feed links.
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
    
    # Remove duplicates
    rss_links = list(set(rss_links))
    print(f"✅ Found {len(rss_links)} unique RSS links.")
    return rss_links

def scrape_articles_from_feed(feed_url, csv_writer):
    """
    Parses an RSS feed and scrapes the content of each article, writing it to a CSV file.
    """
    print(f"\n--- Processing feed: {feed_url} ---")
    feed = feedparser.parse(feed_url)
    print(f"📢 Feed Title: {feed.feed.get('title')}\n")

    for entry in feed.entries:
        print("===")
        print(f"📰 Title: {entry.title}")
        print(f"🔗 Link: {entry.link}")
        print(f"🕒 Published: {entry.published}")

        try:
            response = requests.get(entry.link, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to retrieve article: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='article-content')

        if article_body:
            paragraphs = article_body.find_all('p')
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            print("\n📄 Article Content:")
            print(content[:200] + "...\n")

            csv_writer.writerow([entry.title, entry.link, entry.published, content])
        else:
            print("⚠️ Could not find article content.\n")

def main():
    """
    Main function to orchestrate the scraping process.
    """
    start_time = time.time()
    base_url = "https://vietstock.vn/rss"
    rss_links = scrape_rss_links(base_url)

    if not rss_links:
        print("No RSS links found. Exiting.")
        return

    csv_file = "vietstock_all_articles.csv"
    csv_headers = ["Title", "Link", "Published", "Content"]

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        for link in rss_links:
            scrape_articles_from_feed(link, writer)

    end_time = time.time()
    print(f"✅ All data has been successfully saved to {csv_file}")
    print(f"⏳ Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
