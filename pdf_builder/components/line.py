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
        margin_bottom: float = 0,
        margin_left: float = 0,
        style: dict | None = None,
    ):
        """
        Initialize a line component.

        Args:
            thickness: Line thickness in mm (the line occupies this vertical space)
            color: RGB color tuple (e.g., (255, 102, 0) for orange)
            full_width: If True, line spans full page width ignoring margins
            margin_bottom: Additional space below the line in mm (following CSS convention).
                          - 0 = no gap, line fully visible (default)
                          - Positive values = creates gap below the line
                          Example: thickness=1, margin_bottom=0 → line is 1mm tall, no gap
                                   thickness=1, margin_bottom=5 → line is 1mm tall, 5mm gap below
            margin_left: Left indentation in mm (default: 0)
            style: Additional styling
        """
        super().__init__(style)
        self.thickness = thickness
        self.color = color
        self.full_width = full_width
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left

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
            x1 = 0 + self.margin_left
            x2 = pdf.w
        else:
            x1 = pdf.l_margin + self.margin_left
            x2 = pdf.w - pdf.r_margin

        # Set line style
        pdf.set_line_width(self.thickness)
        pdf.set_draw_color(*self.color)

        # Draw the line (centered on Y coordinate)
        pdf.line(x1, y, x2, y)

        # In fpdf2, lines are centered on the Y coordinate:
        # - A line at Y with thickness T spans from (Y - T/2) to (Y + T/2)
        # - To have no gap, next component should start at Y + T/2
        # Then add margin_bottom for additional spacing (CSS pattern)
        pdf.set_y(y + self.thickness / 2 + self.margin_bottom)

        # Restore margins if they were changed
        if saved_margins:
            pdf.set_margins(saved_margins[0], pdf.t_margin, saved_margins[1])

    def __repr__(self) -> str:
        margin_info = f", margin_bottom={self.margin_bottom}mm" if self.margin_bottom != 0 else ""
        return f"Line(thickness={self.thickness}mm, color={self.color}{margin_info})"
