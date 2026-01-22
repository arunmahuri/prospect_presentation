from src.orchestrator import build_graph
import streamlit as st
from src.utils.logging_config import setup_logging

setup_logging()  # initialize once

st.title("IntentHQ Prospect Presentation Generator")

prospect_name = st.text_input("Prospect Name", value="Nike")
prospect_url = st.text_input("Prospect URL", value="https://www.nike.com")
query = st.text_area(
    "What do you want the presentation to focus on?",
    value="Create a tailored sales deck highlighting how IntentHQ can help this prospect with Customer Insights.",
)

if st.button("Generate Presentation"):
    with st.spinner("Running pipeline..."):
        app = build_graph()
        result = app.invoke(
            {
                "prospect_name": prospect_name,
                "prospect_url": prospect_url,
                "query": query,
            }
        )

    st.subheader("LLM Response")
    st.text(result.get("llm_response", ""))

    st.subheader("Evaluation")
    st.text(result.get("evaluation", ""))

    st.subheader("PPT Path")
    st.code(result.get("ppt_path", ""))