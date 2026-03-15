"""Render context - carries state through the component tree."""

from typing import Any

from fpdf import FPDF
from pydantic import BaseModel


class RenderContext:
    """
    Context object passed through the component tree during rendering.

    Contains:
    - The PDF instance (fpdf2 FPDF object)
    - Optional data model for dynamic content (Pydantic BaseModel)
    - Current rendering state (position, styles, etc.)
    - Shared data between components
    """

    def __init__(self, pdf: FPDF, data: BaseModel | None = None):
        """
        Initialize rendering context.

        Args:
            pdf: The FPDF instance to render to
            data: Optional Pydantic model containing data for dynamic content
                  (e.g., employee name, date, company info)
        """
        self.pdf: FPDF = pdf
        self.data: BaseModel | None = data
        self.state: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set a state value."""
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.state.get(key, default)

    def has(self, key: str) -> bool:
        """Check if state key exists."""
        return key in self.state

    def get_current_y(self) -> float:
        """Get current Y position in the PDF."""
        return self.pdf.get_y()

    def get_current_x(self) -> float:
        """Get current X position in the PDF."""
        return self.pdf.get_x()

    def get_page_width(self) -> float:
        """Get effective page width (excluding margins)."""
        return self.pdf.epw  # Effective page width

    def get_page_height(self) -> float:
        """Get effective page height (excluding margins)."""
        return self.pdf.eph  # Effective page height

    def __repr__(self) -> str:
        return f"RenderContext(pdf={self.pdf.__class__.__name__}, state={self.state})"
