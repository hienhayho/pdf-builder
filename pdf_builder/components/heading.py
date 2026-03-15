"""Heading component - renders headings at different levels."""

from pdf_builder.core import Component, RenderContext


class Heading(Component):
    """
    A heading component for section titles.

    Supports multiple levels (H1, H2, H3, etc.) with automatic sizing.
    """

    # Default sizes for each heading level
    HEADING_SIZES = {
        1: 20,
        2: 16,
        3: 14,
        4: 12,
        5: 11,
        6: 10,
    }

    def __init__(
        self,
        content: str,
        level: int = 1,
        color: tuple[int, int, int] = (0, 0, 0),
        align: str = "L",
        font_family: str = "Arial",
        style: dict | None = None,
    ):
        """
        Initialize a heading.

        Args:
            content: Heading text
            level: Heading level (1-6)
            color: RGB color tuple
            align: Text alignment
            font_family: Font family
            style: Additional styling
        """
        super().__init__(style)
        self.content = content
        self.level = max(1, min(6, level))  # Clamp between 1-6
        self.color = color
        self.align = align
        self.font_family = font_family

    def render(self, context: RenderContext) -> None:
        """Render the heading."""
        pdf = context.pdf

        # Get font size for this level
        font_size = self.HEADING_SIZES[self.level]

        # Get current font family (to preserve Unicode font if set)
        current_font = pdf.font_family or self.font_family

        # Set font (bold for headings)
        pdf.set_font(current_font, "B", font_size)

        # Set color
        pdf.set_text_color(*self.color)

        # Render heading
        pdf.cell(w=0, h=font_size * 0.5, text=self.content, align=self.align, ln=True)

        # Reset text color to black
        pdf.set_text_color(0, 0, 0)

        # Add spacing after heading
        spacing = {1: 5, 2: 4, 3: 3, 4: 2, 5: 2, 6: 1}
        pdf.ln(spacing[self.level])

    def __repr__(self) -> str:
        return f"Heading(level={self.level}, '{self.content}')"
