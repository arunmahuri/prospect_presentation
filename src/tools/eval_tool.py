from src.utils.llm_setup import LLMManager
from src.utils.prompts import EVAL_PROMPT
llm_manager = LLMManager()

def evaluate_response(query: str, response: str) -> str:
    prompt = EVAL_PROMPT.format(query=query, response=response)
    return llm_manager.generate(prompt)