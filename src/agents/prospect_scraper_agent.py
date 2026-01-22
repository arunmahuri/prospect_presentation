from typing import Tuple
from src.tools.scraper_tool import scrape_site
from src.utils.config import ChromaConfig, ProspectConfig
from src.tools.embedding_tool import add_documents, search
from loguru import logger

chroma_cfg = ChromaConfig()
prospect_cfg = ProspectConfig()

max_pages = prospect_cfg.max_pages

class ProspectScraperAgent:
    def run(
        self,
        prospect_name: str,
        prospect_url: str,
        query: str,
    ) -> Tuple[str, list, list]:
        logger.info(
            "ProspectScraperAgent.run called",
            extra={"prospect_name": prospect_name, "prospect_url": prospect_url},
        )

        content, metadatas = scrape_site([prospect_url], max_pages=prospect_cfg.max_pages)
        logger.debug(f"Scraped {len(content)} chunks from {prospect_url}")

        for m in metadatas:
            m["prospect_name"] = prospect_name

        add_documents(
            documents=content,
            metadatas=metadatas,
            collection_name=chroma_cfg.prospect_collection,
        )

        prospect_docs = search(chroma_cfg.intenthq_collection, 
                                    f"how intentHQ helps {prospect_name} industry and predict customer behaviour", k=3)
        prospect_context = "\n".join([doc.page_content for doc in prospect_docs])
        logger.debug(f"Retrieved prospect_docs context: {prospect_context}")

        return prospect_context, content, metadatas