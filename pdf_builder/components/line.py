"""Line component - renders a horizontal line."""

from pdf_builder.core import Component, RenderContext


class Line(Component):
    """
    A horizontal line component.

    Perfect for:
    - Dividers
    - Headers/footers
    - Visual separators
    """

    def __init__(
        self,
        thickness: float = 0.5,
        color: tuple[int, int, int] = (0, 0, 0),
        full_width: bool = False,
        style: dict | None = None,
    ):
        """
        Initialize a line component.

        Args:
            thickness: Line thickness in mm
            color: RGB color tuple (e.g., (255, 102, 0) for orange)
            full_width: If True, line spans full page width ignoring margins
            style: Additional styling
        """
        super().__init__(style)
        self.thickness = thickness
        self.color = color
        self.full_width = full_width

    def render(self, context: RenderContext) -> None:
        """Render a horizontal line across the page."""
        pdf = context.pdf

        # Save current margins if full_width is enabled
        saved_margins = None
        if self.full_width:
            saved_margins = (pdf.l_margin, pdf.r_margin)
            pdf.set_margins(0, pdf.t_margin, 0)

        # Get current Y position
        y = pdf.get_y()

        # Calculate line start and end X positions
        if self.full_width:
            x1 = 0
            x2 = pdf.w
        else:
            x1 = pdf.l_margin
            x2 = pdf.w - pdf.r_margin

        # Set line style
        pdf.set_line_width(self.thickness)
        pdf.set_draw_color(*self.color)

        # Draw the line
        pdf.line(x1, y, x2, y)

        # Move Y position down by line thickness
        pdf.set_y(y + self.thickness)

        # Restore margins if they were changed
        if saved_margins:
            pdf.set_margins(saved_margins[0], pdf.t_margin, saved_margins[1])

    def __repr__(self) -> str:
        return f"Line(thickness={self.thickness}mm, color={self.color})"
