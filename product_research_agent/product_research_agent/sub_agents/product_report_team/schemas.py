"""Schemas for the product report writers team."""

from pydantic import (
    BaseModel,
    Field,
)


# For report_reviewer_agent
class ReviewFeedback(BaseModel):
    """Feedback on the product report."""

    has_feedback: bool = Field(
        description="Whether significant feedback is being provided."
    )
    feedback_summary: str = Field(
        description="A brief summary of the feedback, or a statement if no significant feedback."
    )
    detailed_feedback_points: list[str] | None = Field(
        default=None,
        description="Specific points of feedback for improvement if has_feedback is true.",
    )
