from urllib.parse import urljoin, urlparse
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup
from loguru import logger


class WebScraper:
    def __init__(self, base_urls, max_pages=10):
        self.base_urls = base_urls
        self.max_pages = max_pages
        self.visited = set()
        self.content = []
        self.metadatas = []

    def fetch(self, url: str) -> str:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 ... Chrome/120 Safari/537.36",
            }
        )
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text

    def scrape(self):
        to_visit = self.base_urls[:]

        while to_visit and len(self.visited) < self.max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue
            logger.info(f"Scraping URL: {url}")
            try:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200, chunk_overlap=200
                )
                html = self.fetch(url)
                soup = BeautifulSoup(html, "html.parser")

                for tag in soup(["nav", "footer", "script", "style"]):
                    tag.decompose()

                raw_text = soup.get_text(separator="\n")
                text = "\n".join(
                    line.strip()
                    for line in raw_text.splitlines()
                    if line.strip()
                )

                chunks = splitter.split_text(text)
                for c in chunks:
                    lines = c.split("\n")
                    unique_lines = list(dict.fromkeys(lines))
                    dedup_chunk = "\n".join(unique_lines)
                    if dedup_chunk.strip():
                        self.content.append(dedup_chunk)
                        self.metadatas.append(
                            {
                                "url": url,
                                "title": soup.title.string if soup.title else "",
                                "prospect": urlparse(url).netloc,
                            }
                        )

                self.visited.add(url)

                if len(self.visited) < self.max_pages:
                    links = self._find_links(soup, url)
                    to_visit.extend(links)

                time.sleep(1)

            except Exception as e:
                print(f"Error scraping {url}: {e}")
                self.visited.add(url)
                continue

        return self.content, self.metadatas

    def _find_links(self, soup, base_url):
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            if urlparse(self.base_urls[0]).netloc not in urlparse(full_url).netloc:
                continue
            if full_url not in self.visited:
                links.append(full_url)
        return links[:5]