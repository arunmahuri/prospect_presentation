from typing import List, Tuple
from src.tools.scraper_tool import scrape_site
from src.tools.embedding_tool import add_documents
from src.utils.config import ChromaConfig, IntentHQConfig
from loguru import logger

chroma_cfg = ChromaConfig()
intenthq_cfg = IntentHQConfig()
max_pages = intenthq_cfg.max_pages

class IntentHQIndexerAgent:
    def run(self, intenthq_urls: List[str]) -> Tuple[list, list]:
        logger.info("IntentHQIndexerAgent.run called")
        content, metadatas = scrape_site(intenthq_urls, max_pages=max_pages)
        for m in metadatas:
            m["source"] = "intenthq"
        logger.debug(f"Scraped {len(content)} chunks from IntentHQ")
        add_documents(
            documents=content,
            metadatas=metadatas,
            collection_name=chroma_cfg.intenthq_collection,
        )
        logger.info("IntentHQ indexing completed")
        return content, metadatas