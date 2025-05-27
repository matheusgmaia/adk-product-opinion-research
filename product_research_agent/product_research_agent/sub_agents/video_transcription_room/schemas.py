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

"""Pydantic schemas for video transcription."""

from pydantic import (
    BaseModel,
    Field,
)


class TranscriptSegment(BaseModel):
    """A single segment of a video transcript."""

    text: str = Field(description="The text of the transcript segment.")
    start: float = Field(description="The start time of the segment in seconds.")
    duration: float = Field(description="The duration of the segment in seconds.")


class VideoTranscript(BaseModel):
    """Structured transcript and metadata for a single video."""

    video_id: str = Field(description="The YouTube video ID.")
    link: str = Field(description="The YouTube video URL.")
    channel: str | None = Field(
        default=None, description="The YouTube channel name, if available."
    )
    transcript: list[TranscriptSegment] = Field(
        description="List of transcript segments."
    )
    status: str = Field(
        description="Status of transcript retrieval (e.g., 'success', 'rejected')."
    )
    message: str | None = Field(
        default=None,
        description="Error message if status is 'rejected', or other relevant info.",
    )


class AllVideoTranscripts(BaseModel):
    """The overall structured output containing all video transcripts and the product name."""

    product_name: str = Field(description="The name of the product being researched.")
    transcripts: list[VideoTranscript] = Field(
        description="A list of transcripts for the analyzed videos."
    )
