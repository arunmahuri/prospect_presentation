RAG_PROMPT="""
    You are a sales presentation assistant.
    Presentation Context: {query} 
    Use the following context about IntentHQ:
    ***{intenthq_context}***
    Use the following context about the prospect {prospect_name}:
    ***{prospect_context}***
    Create a presentation with 7 slides.
    For each slide, output:
    - Slide Title
    - 3-5 bullet points
    - 1 short explanation (2 sentences max)
    Follow this exact structure:
    Slide 1: Introduction
    - IntentHQ value proposition
    - {prospect_name} industry overview
    - {prospect_name} challenges
    - Relevant examples
    Slide 2: Understanding IntentHQ
    - What IntentHQ is
    - How it works
    - Why it is valuable for {prospect_name}
    Slide 3: Unlocking Customer Insights
    - Real-world insights
    - How IntentHQ helps {prospect_name}
    - Example use cases
    Slide 4: Personalized Marketing
    - What personalization means
    - How IntentHQ personalizes for {prospect_name}
    - Examples
    Slide 5: Customer Segmentation
    - Definition
    - How IntentHQ helps {prospect_name}
    - Example use cases
    Slide 6: AI-Powered Retail Insights
    - What AI is
    - How IntentHQ uses AI
    - Examples
    Slide 7: Call to Action
    - Summary
    - Next steps
  """

EVAL_PROMPT = """
    You are an evaluator. Given the user query and the model response,
    rate the response on:
    - relevance (0-10)
    - specificity (0-10)
    - correctness (0-10)

    Return a short textual assessment and the three scores.

    User query:
    {query}

    Model response:
    {response}
"""

INTENTHQ_SEARCH_PROMPT = """
    Conmpany Overview; Customer Behavioral insights; Early churn reduction, Predictive customer behaviour; 
    Customer Engagement; Personalized marketing strategies; AI-driven retail insights; 
    Customer segmentation; Use Cases; Success Stories; Resources for {prospect_name}
"""