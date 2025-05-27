# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_websearch_agent for finding research papers using search tools."""

from crewai_tools import FileWriterTool
from google.adk import Agent
from google.adk.tools.crewai_tool import CrewaiTool
from google.genai import types

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

file_writer = Agent(
    name="file_writer",
    model=MODEL,
    description="Saves a report markdown document.",
    instruction=prompt.FILE_WRITER_PROMPT,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[
        CrewaiTool(
            name="file_writer_tool",
            description=("Writes a file to disk"),
            tool=FileWriterTool(),
        )
    ],
)
