"""Data models for table cells with span support."""

from pydantic import BaseModel, Field

from pdf_builder.core import Component


class TableCell(BaseModel):
    """
    A table cell with optional rowspan and colspan.

    Example:
        TableCell(text="A1", rowspan=2, colspan=1)
        TableCell(text=InlineText(...), rowspan=1, colspan=2)
    """

    text: str | Component = Field(..., description="Cell content (string or Component)")
    rowspan: int = Field(default=1, description="Number of rows to span")
    colspan: int = Field(default=1, description="Number of columns to span")

    class Config:
        arbitrary_types_allowed = True  # Allow Component types
