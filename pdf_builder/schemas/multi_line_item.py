"""Schema for multi-line text items with individual styling."""

from pydantic import BaseModel, Field

from .inline_segment import FontStyle


class MultiLineItem(BaseModel):
    """
    Represents a single line in a multi-line text with individual styling.

    Each line can have its own font size, style, and color, allowing for
    rich multi-line text formatting like titles with varying emphasis.

    Args:
        text: The text content for this line
        font_size: Font size in points (optional, inherits from parent if not set)
        font_style: Font style - REGULAR, BOLD, ITALIC, BOLD_ITALIC
                   (optional, inherits from parent if not set)
        color: RGB tuple (r, g, b) where each value is 0-255
              (optional, inherits from parent if not set)

    Example:
        >>> from pdf_builder.schemas import MultiLineItem, FontStyle
        >>> title_items = [
        ...     MultiLineItem(
        ...         text="CHƯƠNG TRÌNH ĐÀO TẠO",
        ...         font_size=16,
        ...         font_style=FontStyle.BOLD
        ...     ),
        ...     MultiLineItem(
        ...         text="Năm 2026",
        ...         font_size=14,
        ...         font_style=FontStyle.BOLD_ITALIC,
        ...         color=(255, 102, 0)
        ...     )
        ... ]
    """

    text: str = Field(..., description="The text content for this line")
    font_size: int | None = Field(
        default=None, description="Font size in points (inherits from parent if None)"
    )
    font_style: FontStyle | None = Field(
        default=None,
        description="Font style (inherits from parent if None)",
    )
    color: tuple[int, int, int] | None = Field(
        default=None,
        description="RGB color tuple (0-255 for each component, inherits from parent if None)",
    )

    class Config:
        use_enum_values = True  # Use enum values ("B") instead of enum objects
