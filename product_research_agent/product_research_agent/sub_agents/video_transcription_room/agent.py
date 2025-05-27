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

from google.adk import Agent
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import JSONFormatter

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"


# pylint: disable=W0102
def download_youtube_transcript(
    video_id: str, language_codes: list[str] = ["en"]
) -> dict[str, str]:
    """
    Downloads the transcript for a given YouTube video ID.

    Args:
        video_id (str): The ID of the YouTube video.
                        (e.g., for URL https://www.youtube.com/watch?v=dQw4w9WgXcQ,
                         the video_id is 'dQw4w9WgXcQ')
        language_codes (list[str], optional): A list of language codes to try, in order of preference.
                                         Defaults to ['en'] (English).

    Returns:
        dict[str, str]: The status for the call and the message that can be the transcript or the error message.
    """
    try:
        print(
            f"Attempting to fetch transcript for video ID: {video_id} in languages: {language_codes}"
        )

        # Get a list of available transcripts
        transcript_list = YouTubeTranscriptApi().list(video_id)

        # Try to find a transcript in the preferred languages
        transcript = transcript_list.find_transcript(language_codes)

        # Fetch the actual transcript data (list of dictionaries)
        transcript_data = transcript.fetch()

        formatter = JSONFormatter()
        full_transcript = formatter.format_transcript(transcript_data)

        print(f"Successfully fetched transcript for video ID: {video_id}")
        return {"status": "success", "message": full_transcript}

    except TranscriptsDisabled:
        return {
            "status": "rejected",
            "message": f"Error: Transcripts are disabled for video ID: {video_id}",
        }
    except NoTranscriptFound:
        try:
            available_transcripts = YouTubeTranscriptApi().list(video_id)
            message_lines = ["Available transcripts for this video:"]
            for available_transcript in available_transcripts:
                message_lines.append(
                    f"  - Language: {available_transcript.language} ({available_transcript.language_code}), "
                    f"Type: {'manual' if not available_transcript.is_generated else 'auto-generated'}"
                )
            return {"status": "rejected", "message": "\n".join(message_lines)}
        except Exception as e_list:  # pylint: disable=broad-exception-caught
            return {
                "status": "rejected",
                "message": f"Could not list transcripts for {video_id} after NoTranscriptFound: {e_list}",
            }
    except Exception as e_unexpected:  # pylint: disable=broad-exception-caught
        return {
            "status": "rejected",
            "message": f"An unexpected error occurred for video ID {video_id}: {e_unexpected}",
        }


transcript_agent = Agent(
    model=MODEL,
    name="video_transcript_agent",
    instruction=prompt.TRANSCRIPT_AGENT_PROMPT,  # Use prompt from prompt.py
    output_key="videos_transcript",
    description="Agent that uses tool download_youtube_transcript to fetch YouTube video transcripts and structures the combined output as a JSON string conforming to the AllVideoTranscripts schema.",
    tools=[download_youtube_transcript],
)
