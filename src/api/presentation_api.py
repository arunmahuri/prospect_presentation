from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestrator import build_graph
from src.utils.logging_config import setup_logging

setup_logging()  # initialize once

app = FastAPI(title="IntentHQ Prospect Pipeline API")
graph_app = build_graph()


class PipelineRequest(BaseModel):
    prospect_name: str
    prospect_url: str
    query: str


@app.post("/run")
def run_pipeline(req: PipelineRequest):
    state = {
        "prospect_name": req.prospect_name,
        "prospect_url": req.prospect_url,
        "query": req.query,
    }
    result = graph_app.invoke(state)
    return {
        "llm_response": result.get("llm_response"),
        "evaluation": result.get("evaluation"),
        "ppt_path": result.get("ppt_path"),
    }