"""Product_research:"""

import json

from google.adk.agents import (
    LlmAgent,
    SequentialAgent,
)
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from langchain_community.tools import YouTubeSearchTool
from youtube_search import YoutubeSearch

from . import prompt
from .sub_agents.file_writer import file_writer
from .sub_agents.product_report_team import product_report_team
from .sub_agents.video_transcription_room import transcript_agent

MODEL = "gemini-2.5-pro-preview-05-06"


def append_to_state(
    tool_context: ToolContext, field: str, response: str
) -> dict[str, str]:
    """Append new output to an existing state key.

    Args:
        field (str): a field name to append to
        response (str): a string to append to the field

    Returns:
        dict[str, str]: {"status": "success"}
    """
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    return {"status": "success"}


def youtube_search(query: str, num_results: int) -> str:
    """
    Searches YouTube for videos matching the given query and returns a list of video URLs.

    Args:
        query (str): The search query to look for on YouTube.
        num_results (int): The number of search results to retrieve.

    Returns:
        str: A string representation of a list containing the URLs of the videos found.
    """
    results = YoutubeSearch(query, num_results).to_json()
    data = json.loads(results)
    url_suffix_list = [
        "https://www.youtube.com" + video["url_suffix"] for video in data["videos"]
    ]
    return str(url_suffix_list)


product_research_team = SequentialAgent(
    name="product_research_team",
    description="Write a report about information and opinions gathered about the product.",
    sub_agents=[transcript_agent, product_report_team, file_writer],
)

youtube_search_tool = YouTubeSearchTool(
    name="youtube_search_tool",
    description="Search for youtube videos. Use the run method with a query string to search for videos.",
)

product_research_agent = LlmAgent(
    name="product_research_agent",
    model=MODEL,
    description="Guides the user in inputting youtube videos that talk about a specific product.",
    instruction=prompt.GREETER_PROMPT,
    sub_agents=[product_research_team],
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[youtube_search, append_to_state],
)

root_agent = product_research_agent
