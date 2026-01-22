from src.tools.eval_tool import evaluate_response
from loguru import logger


class EvaluatorAgent:
    def run(self, query: str, response: str) -> str:
        logger.info("EvaluatorAgent.run called")
        return evaluate_response(query, response)