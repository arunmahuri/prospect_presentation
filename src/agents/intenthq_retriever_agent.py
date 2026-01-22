from src.utils.config import ChromaConfig
from loguru import logger
from src.tools.embedding_tool import search
from src.utils.prompts import INTENTHQ_SEARCH_PROMPT

chroma_cfg = ChromaConfig()


class IntentHQRetrieverAgent:
    def run(self, prospect_name: str) -> str:
        logger.info("IntentHQRetrieverAgent.run called")
        intenthq_docs = search(chroma_cfg.intenthq_collection, INTENTHQ_SEARCH_PROMPT.format(prospect_name=prospect_name), k=3)
        intenthq_context = "\n".join([doc.page_content for doc in intenthq_docs])
        logger.debug(f"Retrieved IntentHQ context: {intenthq_context}")
        return intenthq_context