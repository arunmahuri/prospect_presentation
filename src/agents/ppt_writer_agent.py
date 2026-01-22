from src.tools.ppt_tool import save_response_to_ppt
from loguru import logger


class PPTWriterAgent:
    def run(self, llm_response: str, output_path: str, prospect_url: str) -> str:
        logger.info("PPTWriterAgent.run called")
        return save_response_to_ppt(llm_response, output_path, prospect_url)