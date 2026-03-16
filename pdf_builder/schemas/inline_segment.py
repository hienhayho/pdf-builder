"""Data models for inline text segments."""

from enum import Enum

from pydantic import BaseModel, Field


class FontStyle(str, Enum):
    """Font style options for text rendering."""

    REGULAR = ""
    BOLD = "B"
    ITALIC = "I"
    BOLD_ITALIC = "BI"
    UNDERLINE = "U"


class InlineSegment(BaseModel):
    """
    A segment of text with specific styling for inline rendering.

    Example:
        InlineSegment(text="Bold text", style=FontStyle.BOLD)
        InlineSegment(text="Red text", style=FontStyle.REGULAR, color=(255, 0, 0))
    """

    text: str = Field(..., description="The text content to render")
    style: FontStyle = Field(
        default=FontStyle.REGULAR, description="Font style (bold, italic, etc.)"
    )
    color: tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="RGB color tuple (0-255 for each component)",
    )

    class Config:
        use_enum_values = True  # Use enum values ("B") instead of enum objects
