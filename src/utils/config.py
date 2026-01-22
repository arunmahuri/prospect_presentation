from dataclasses import dataclass
from typing import List
import os

@dataclass
class LLMConfig:
    model_path: str = os.path.join(
        os.path.dirname(__file__),
        "../../models/",
        "mistral-7b-instruct-q4_k_m.gguf")
    temperature: float = 0.3
    max_tokens: int = 1024
    n_ctx: int = 4096
    n_gpu_layers: int = -1
    top_k: int = 50
    top_p: float = 0.9


@dataclass
class EmbeddingConfig:
    model_name: str = "BAAI/bge-small-en-v1.5"


@dataclass
class ChromaConfig:
    persist_dir: str = "vector/chroma_db"
    prospect_collection: str = "prospect_docs"
    intenthq_collection: str = "intenthq_docs"

@dataclass
class LoggingConfig:
    LOG_LEVEL: str = "DEBUG"          # DEBUG, INFO, WARNING, ERROR
    LOG_DIR: str = "logs"          # folder for log files

@dataclass
class ProspectConfig:
    max_pages: int = 30

@dataclass
class IntentHQConfig:
    # You can adjust these URLs as needed
    urls: List[str] = (
        "https://intenthq.com/",    
        "https://intenthq.com/platform/",
        "https://intenthq.com/use-cases/",
        "https://intenthq.com/values/",
        "https://intenthq.com/about-us/",
        "https://intenthq.com/success-stories/",
        "https://intenthq.com/solutions",
        "https://intenthq.com/resources/"
    )
    max_pages: int = 70
    do_force_index: bool = False
    logo_path: str = "presentations/logos/intenthq_logo_bkp.png"