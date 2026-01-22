from src.utils.llm_setup import LLMManager
from src.utils.prompts import RAG_PROMPT
from loguru import logger
llm_manager = LLMManager()

class RAGComposerAgent:
    def run(
        self,
        prospect_name: str,
        query: str,
        prospect_context: str,
        intenthq_context: str,
    ) -> str:
        logger.info("RAGComposerAgent.run called")
        prompt = RAG_PROMPT.format(
            prospect_name=prospect_name,
            query=query,
            prospect_context=prospect_context,
            intenthq_context=intenthq_context,
        )
        logger.debug(f"RAGComposerAgent prompt: {prompt}")
        response = llm_manager.generate(prompt)
        logger.debug(f"RAGComposerAgent response: {response}")
        return response