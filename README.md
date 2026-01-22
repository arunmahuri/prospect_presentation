# Automated Prospect Presentation Generator

An AI-powered system that automatically generates tailored sales presentations for prospective clients using Retrieval-Augmented Generation (RAG) with local LLM and vector database.

## Overview
The IntentHQ Prospect Presentation Generator is an end‑to‑end, agent‑orchestrated system that builds tailored sales presentations for any prospect. It combines:
- Dynamic web scraping
- One‑time IntentHQ knowledge indexing
- Chroma vector search
- Local LLM inference (Mistral 7B)
- LangGraph state‑based orchestration
- Automated PPT generation with logos
- Evaluation and logging
- Streamlit UI, FastAPI service, and CLI runner
This architecture ensures a scalable, reproducible, and privacy‑preserving workflow for generating high‑quality, personalized sales decks.

## Installation
1. Clone the repository
git clone https://github.com/arunmahuri/prospect_presentation.git
cd prospect_presentation


2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate


3. Install dependencies
pip install -e .


4. Download the LLM model
Place your .gguf model (e.g., mistral-7b-instruct-q4_k_m.gguf) in a local directory and update the path in config.py.

## Configuration
All configuration lives in config.py:
- LLM settings
- Embedding model
- Chroma DB paths
- IntentHQ URLs
- Logging settings (LOG_LEVEL, LOG_DIR)
Example:
@dataclass
class LoggingConfig:
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"

## Running the Application
🖥️ 1. Streamlit UI
streamlit run src/ui/demo_ui.py


Open the browser → fill in:
- Prospect Name
- Prospect URL
- Query
Click Generate Presentation.

🌐 2. FastAPI Server
Start the API:
uvicorn src.api.presentation_api:app --reload


Send a request:
curl -X POST "http://127.0.0.1:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_name": "Nike",
    "prospect_url": "https://nike.com",
    "query": "Create a tailored sales deck"
  }'



🖥️ 3. CLI Runner
python -m src.cli.run_orchestrator \
  --prospect-name "Nike" \
  --prospect-url "https://nike.com" \
  --query "Create a tailored sales deck"



## How the Pipeline Works
1. check_intenthq
Determines whether IntentHQ has already been indexed.
2. index_intenthq (conditional)
Runs only once; skips on future runs.
3. scrape_prospect
Scrapes and embeds the prospect website.
4. retrieve_intenthq
Retrieves relevant IntentHQ content.
5. compose_rag
Builds a combined prompt and calls the LLM.
6. evaluate
Scores the LLM output.
7. write_ppt
Generates a PPT with:
- Title
- Bullets
- Prospect logo
- IntentHQ logo

## Logging
Logging is handled by Loguru.
- Console logs (INFO+)
- Rotating file logs in ./logs/app.log (DEBUG+)
Configured in logging_config.py.

