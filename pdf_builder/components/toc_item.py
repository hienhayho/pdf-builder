"""TOC Item component - table of contents item with number and title."""

from pdf_builder.core import Component, RenderContext


class TocItem(Component):
    """
    A table of contents item component with a large number and title text.

    Perfect for:
    - Table of contents entries
    - Numbered lists with large visual numbers
    """

    def __init__(
        self,
        number: int | str,
        title: str,
        number_color: tuple[int, int, int] = (0, 102, 204),  # Blue
        title_color: tuple[int, int, int] = (80, 80, 80),  # Dark gray
        number_font_size: float = 24,
        title_font_size: float = 14,
        number_width: float = 15,  # Width reserved for number in mm
        style: dict | None = None,
    ):
        """
        Initialize a TOC item component.

        Args:
            number: The number to display (e.g., "1", "2", etc.)
            title: The title text
            number_color: RGB tuple for number color
            title_color: RGB tuple for title color
            number_font_size: Font size for the number
            title_font_size: Font size for the title
            number_width: Width reserved for the number column in mm
            style: Additional styling
        """
        super().__init__(style)
        self.number = str(number)
        self.title = title
        self.number_color = number_color
        self.title_color = title_color
        self.number_font_size = number_font_size
        self.title_font_size = title_font_size
        self.number_width = number_width

    def render(self, context: RenderContext) -> None:
        """Render the TOC item with number on left and title on right."""
        pdf = context.pdf

        # Save current position
        start_x = pdf.get_x()
        start_y = pdf.get_y()

        # Render the number (large, blue, bold)
        pdf.set_font(pdf.font_family or "DejaVu", style="B", size=self.number_font_size)
        pdf.set_text_color(*self.number_color)
        pdf.set_xy(start_x, start_y)
        pdf.cell(w=self.number_width, h=10, txt=self.number, ln=0, align="L")

        # Render the title (smaller, gray)
        pdf.set_font(pdf.font_family or "DejaVu", style="", size=self.title_font_size)
        pdf.set_text_color(*self.title_color)
        pdf.set_xy(start_x + self.number_width, start_y)
        # Use multi_cell for title to support wrapping
        title_width = context.get_page_width() - self.number_width
        pdf.multi_cell(w=title_width, h=6, txt=self.title, align="L")

        # Reset text color
        pdf.set_text_color(0, 0, 0)

    def __repr__(self) -> str:
        return f"TocItem(number={self.number}, title='{self.title}')"
