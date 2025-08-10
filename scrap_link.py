import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://vietstock.vn/rss"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

rss_links = []

# Look for <a> tags with href ending in .rss or .xml
count = 0
for a in soup.find_all("a", href=True):
    href = a["href"]
    if ".rss" in href or ".xml" in href:
        full_url = urljoin(url, href)
        rss_links.append(full_url)
        count += 1

# Remove duplicates and print
rss_links = list(set(rss_links))
for link in rss_links:
    print(link)
print(f"Found {count} RSS links")    