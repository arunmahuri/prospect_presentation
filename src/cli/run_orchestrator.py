import argparse
from src.orchestrator import build_graph
from src.utils.logging_config import setup_logging

setup_logging()  # initialize once


def main():
    parser = argparse.ArgumentParser(
        description="Run IntentHQ Prospect Pipeline from console"
    )
    parser.add_argument("--prospect-name", required=True, help="Prospect name")
    parser.add_argument("--prospect-url", required=True, help="Prospect URL")
    parser.add_argument("--query", required=True, help="User query")
    args = parser.parse_args()

    app = build_graph()
    state = {
        "prospect_name": args.prospect_name,
        "prospect_url": args.prospect_url,
        "query": args.query,
    }
    result = app.invoke(state)

    print("\n=== LLM Response ===\n")
    print(result.get("llm_response", ""))

    print("\n=== Evaluation ===\n")
    print(result.get("evaluation", ""))

    print("\n=== PPT Path ===\n")
    print(result.get("ppt_path", ""))


if __name__ == "__main__":
    main()