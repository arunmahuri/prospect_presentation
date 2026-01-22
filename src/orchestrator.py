from datetime import datetime
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from src.tools.intenthq_index_utils import intenthq_index_exists
from src.utils.config import IntentHQConfig
from src.agents.prospect_scraper_agent import ProspectScraperAgent
from src.agents.intenthq_indexer_agent import IntentHQIndexerAgent
from src.agents.intenthq_retriever_agent import IntentHQRetrieverAgent
from src.agents.rag_composer_agent import RAGComposerAgent
from src.agents.ppt_writer_agent import PPTWriterAgent
from src.agents.evaluator_agent import EvaluatorAgent


class PipelineState(TypedDict, total=False):
    prospect_name: str
    prospect_url: str
    query: str

    prospect_context: Optional[str]
    intenthq_context: Optional[str]
    llm_response: Optional[str]
    evaluation: Optional[str]
    ppt_path: Optional[str]

    intenthq_indexed: bool


def node_check_intenthq(state: PipelineState) -> PipelineState:
    state["intenthq_indexed"] = intenthq_index_exists()
    return state


def node_index_intenthq(state: PipelineState) -> PipelineState:
    cfg = IntentHQConfig()
    indexer = IntentHQIndexerAgent()
    indexer.run(list(cfg.urls))
    state["intenthq_indexed"] = True
    return state


def node_scrape_prospect(state: PipelineState) -> PipelineState:
    agent = ProspectScraperAgent()
    ctx, _, _ = agent.run(
        prospect_name=state["prospect_name"],
        prospect_url=state["prospect_url"],
        query=state["query"],
    )
    state["prospect_context"] = ctx
    return state


def node_retrieve_intenthq(state: PipelineState) -> PipelineState:
    agent = IntentHQRetrieverAgent()
    ctx = agent.run(state["prospect_name"])
    state["intenthq_context"] = ctx
    return state


def node_compose_rag(state: PipelineState) -> PipelineState:
    agent = RAGComposerAgent()
    resp = agent.run(
        prospect_name=state["prospect_name"],
        query=state["query"],
        prospect_context=state.get("prospect_context", "") or "",
        intenthq_context=state.get("intenthq_context", "") or "",
    )
    state["llm_response"] = resp
    return state


def node_evaluate(state: PipelineState) -> PipelineState:
    agent = EvaluatorAgent()
    eval_text = agent.run(
        query=state["query"],
        response=state["llm_response"],
    )
    state["evaluation"] = eval_text
    return state


def node_write_ppt(state: PipelineState) -> PipelineState:
    agent = PPTWriterAgent()
    output_path = f"presentations/{state['prospect_name'].replace(' ', '_')}_Presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
    ppt_path = agent.run(state["llm_response"], output_path, state["prospect_url"])
    state["ppt_path"] = ppt_path
    return state


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("check_intenthq", node_check_intenthq)
    graph.add_node("index_intenthq", node_index_intenthq)
    graph.add_node("scrape_prospect", node_scrape_prospect)
    graph.add_node("retrieve_intenthq", node_retrieve_intenthq)
    graph.add_node("compose_rag", node_compose_rag)
    graph.add_node("evaluate", node_evaluate)
    graph.add_node("write_ppt", node_write_ppt)

    graph.set_entry_point("check_intenthq")

    def route_after_check(state: PipelineState) -> str:
        if state.get("intenthq_indexed", False):
            return "skip"
        return "index"

    graph.add_conditional_edges(
        "check_intenthq",
        route_after_check,
        {
            "skip": "scrape_prospect",
            "index": "index_intenthq",
        },
    )

    graph.add_edge("index_intenthq", "scrape_prospect")
    graph.add_edge("scrape_prospect", "retrieve_intenthq")
    graph.add_edge("retrieve_intenthq", "compose_rag")
    graph.add_edge("compose_rag", "evaluate")
    graph.add_edge("evaluate", "write_ppt")
    graph.add_edge("write_ppt", END)

    app = graph.compile()
    return app