import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import feedparser
import csv
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://vietstock.vn/rss"

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
        logging.error(f"Failed to retrieve RSS links page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rss_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".rss" in href or ".xml" in href:
            full_url = urljoin(url, href)
            rss_links.append(full_url)
    
    rss_links = list(set(rss_links))
    logging.info(f"Found {len(rss_links)} unique RSS links.")
    return rss_links

def _scrape_articles_from_feed(feed_url: str, csv_writer, current_char_count: int, max_chars: int) -> (int, bool):
    """
    Parses an RSS feed and scrapes the content of each article.
    (Internal helper function)
    Returns the updated character count and a boolean indicating if the max_chars limit was reached.
    """
    logging.info(f"Processing feed: {feed_url}")
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        if max_chars and current_char_count >= max_chars:
            logging.info(f"Max character limit ({max_chars}) reached. Stopping scraping.")
            return current_char_count, True

        logging.info(f"Scraping: {entry.title}")
        try:
            response = requests.get(entry.link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve article '{entry.title}': {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='article-content')

        if article_body:
            paragraphs = article_body.find_all('p')
            content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            
            # Check if adding this content would exceed the limit
            if max_chars and (current_char_count + len(content)) > max_chars:
                logging.info(f"Adding article '{entry.title}' would exceed max character limit ({max_chars}). Stopping scraping.")
                return current_char_count, True

            csv_writer.writerow([entry.title, entry.link, entry.published, content])
            current_char_count += len(content)
        else:
            logging.warning(f"Could not find article content for: {entry.link}")
    
    return current_char_count, False

def scrape_vietstock_articles(max_chars: int = None) -> Dict[str, str]:
    """
    Main function to orchestrate the Vietstock article scraping process.
    Finds all RSS feeds and scrapes articles, saving them to a CSV file.
    Stops scraping if max_chars limit is provided and reached.

    Args:
        max_chars (int, optional): Maximum number of characters to scrape. Defaults to None.

    Returns:
        A dictionary containing the path to the generated CSV file and a message.
    """
    start_time = time.time()
    rss_links = _scrape_rss_links(BASE_URL)

    if not rss_links:
        return {"message": "No RSS links found. Scraping aborted.", "file_path": None}

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    csv_file = os.path.join(output_dir, f"vietstock_articles_{int(time.time())}.csv")
    csv_headers = ["Title", "Link", "Published", "Content"]
    
    current_char_count = 0
    max_chars_reached = False

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        for link in rss_links:
            current_char_count, max_chars_reached = _scrape_articles_from_feed(link, writer, current_char_count, max_chars)
            if max_chars_reached:
                break # Stop processing further feeds

    end_time = time.time()
    total_time = f"{end_time - start_time:.2f}"
    logging.info(f"All data has been successfully saved to {csv_file}")
    logging.info(f"Total execution time: {total_time} seconds")
    
    message = f"Scraping completed in {total_time} seconds."
    if max_chars_reached:
        message += f" (Stopped due to character limit of {max_chars} reached)."

    return {
        "message": message,
        "file_path": csv_file
    }
