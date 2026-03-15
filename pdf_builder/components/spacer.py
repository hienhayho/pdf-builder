"""Spacer component - adds vertical or horizontal space."""

from pdf_builder.core import Component, RenderContext


class Spacer(Component):
    """
    A spacer component for adding whitespace.

    Useful for:
    - Vertical spacing between sections
    - Layout adjustments
    - Visual breathing room
    """

    def __init__(self, height: float = 5, style: dict | None = None):
        """
        Initialize a spacer.

        Args:
            height: Space height in mm
            style: Additional styling
        """
        super().__init__(style)
        self.height = height

    def render(self, context: RenderContext) -> None:
        """Render the spacer (add vertical space)."""
        context.pdf.ln(self.height)

    def __repr__(self) -> str:
        return f"Spacer(height={self.height}mm)"
