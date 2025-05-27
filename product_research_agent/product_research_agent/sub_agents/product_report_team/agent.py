"""product_report_writers_team Agents"""

from google.adk import Agent
from google.adk.agents import LoopAgent  # LoopAgent is already imported
from google.genai import types as genai_types  # For GenerateContentConfig

from . import prompt
from .schemas import ReviewFeedback

MODEL = "gemini-2.5-pro-preview-05-06"

# Configuration for forcing JSON output from the LLM
json_response_config = genai_types.GenerateContentConfig(
    response_mime_type="application/json"
)

# research_agent = Agent(
#     model=MODEL,
#     name="research_agent",
#     description="Analyzes video transcripts to extract key information and facts about a product.",
#     instruction=prompt.RESEARCH_AGENT_PROMPT,
#     output_schema=ExtractedInsights,
#     generate_content_config=json_response_config,
#     output_key="research_results",
#     tools=[google_search],
# )

report_writer_agent = Agent(
    name="report_writer_agent",
    model=MODEL,
    description="Writes and refines a product research report based on transcript analysis and review feedback.",
    instruction=prompt.REPORT_WRITER_AGENT_PROMPT_,
    output_key="product_report",
)

report_reviewer_agent = Agent(
    name="report_reviewer_agent",
    model=MODEL,
    description="Reviews the product report for accuracy, completeness, clarity, and objectivity based on extracted insights and provides structured feedback.",
    instruction=prompt.REPORT_REVIEWER_AGENT_PROMPT_,
    output_schema=ReviewFeedback,
    generate_content_config=json_response_config,
    output_key="critical_feedback",
)


product_report_team = LoopAgent(
    name="ProductReportTeam",
    description="Iteratively researches transcripts, writes, and reviews to generate a comprehensive product report.",
    sub_agents=[
        report_writer_agent,  # Then, write/update the report
        report_reviewer_agent,  # Finally, review the report
    ],
    max_iterations=2,
)
