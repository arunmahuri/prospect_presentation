from typing import List, Tuple
from src.utils.scraper import WebScraper


def scrape_site(base_urls: List[str], max_pages: int = 10) -> Tuple[list, list]:
    scraper = WebScraper(base_urls=base_urls, max_pages=max_pages)
    content, metadatas = scraper.scrape()
    return content, metadatas