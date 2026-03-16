"""Schema for table configuration."""

from enum import Enum

from pydantic import BaseModel, Field


class TextAlign(str, Enum):
    """Text alignment options for table cells."""

    LEFT = "L"
    CENTER = "C"
    RIGHT = "R"


class ColumnConfig(BaseModel):
    """
    Configuration for a single table column.

    Args:
        align: Text alignment for this column (LEFT, CENTER, or RIGHT)
        width: Column width in mm (optional)
    """

    align: TextAlign = Field(
        default=TextAlign.LEFT, description="Text alignment for this column"
    )
    width: float | None = Field(
        default=None, description="Column width in mm (optional)"
    )

    class Config:
        use_enum_values = True


class TableConfig(BaseModel):
    """
    Configuration for table layout and styling.

    Args:
        columns: List of column configurations
        header_fill_color: RGB color for header background
        header_text_color: RGB color for header text
        row_fill_color: RGB color for data rows
        font_size: Font size for table text

    Example:
        >>> from pdf_builder import TableConfig, ColumnConfig, TextAlign
        >>>
        >>> config = TableConfig(
        ...     columns=[
        ...         ColumnConfig(align=TextAlign.CENTER, width=20),
        ...         ColumnConfig(align=TextAlign.LEFT, width=50),
        ...         ColumnConfig(align=TextAlign.RIGHT, width=30),
        ...     ]
        ... )
    """

    columns: list[ColumnConfig] = Field(
        ..., description="List of column configurations"
    )
    header_fill_color: tuple[int, int, int] | None = Field(
        default=(200, 220, 255), description="RGB color for header background"
    )
    header_text_color: tuple[int, int, int] = Field(
        default=(0, 0, 0), description="RGB color for header text"
    )
    row_fill_color: tuple[int, int, int] | None = Field(
        default=(240, 240, 240), description="RGB color for data rows"
    )
    font_size: int = Field(default=10, description="Font size for table text")
