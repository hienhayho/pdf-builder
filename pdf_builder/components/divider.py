"""Divider component for decorative horizontal lines."""

from pdf_builder.core import Component, RenderContext


class Divider(Component):
    """
    Renders a centered horizontal divider line.

    Unlike Line which spans the full width, Divider creates a shorter
    decorative line centered on the page, commonly used under titles or
    to separate sections visually.

    Args:
        width_percent: Width as percentage of page width (default: 40)
        thickness: Line thickness in mm (default: 1)
        color: RGB tuple (r, g, b) where each value is 0-255
        style: Additional style dictionary

    Example:
        >>> # Create orange divider at 30% page width
        >>> divider = Divider(
        ...     width_percent=30,
        ...     thickness=1,
        ...     color=(255, 102, 0)
        ... )
    """

    def __init__(
        self,
        width_percent: float = 40,
        thickness: float = 1,
        color: tuple[int, int, int] = (0, 0, 0),
        style: dict | None = None,
    ):
        super().__init__(style)
        self.width_percent = width_percent
        self.thickness = thickness
        self.color = color

    def render(self, context: RenderContext) -> None:
        """
        Render a centered horizontal divider line.

        Args:
            context: Rendering context containing the PDF instance
        """
        pdf = context.pdf

        # Calculate divider dimensions
        page_width = context.get_page_width()
        divider_width = page_width * (self.width_percent / 100)

        # Calculate centered x position
        x_start = pdf.l_margin + (page_width - divider_width) / 2
        y = pdf.get_y()

        # Set line color and thickness
        pdf.set_draw_color(*self.color)
        pdf.set_line_width(self.thickness)

        # Draw the centered line
        pdf.line(x_start, y, x_start + divider_width, y)

        # Move cursor down by line thickness to avoid overlap
        pdf.ln(self.thickness)

        # Reset draw color to black
        pdf.set_draw_color(0, 0, 0)
