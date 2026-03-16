"""ScoreBoxes component - visual score indicator with colored boxes."""

from pdf_builder.core import Component, RenderContext


class ScoreBoxes(Component):
    """
    Render a visual score indicator using colored boxes.

    Shows current score vs total using filled and empty boxes.
    Perfect for visualizing scores like 2.5/3.

    Example:
        ScoreBoxes(current=2.5, total=3)  # Shows 2.5 filled boxes out of 3
    """

    def __init__(
        self,
        current: float,
        total: int = 3,
        box_width: float = 25,
        box_height: float = 8,
        spacing: float = 2,
        filled_color: tuple[int, int, int] = (66, 133, 244),  # Blue
        empty_color: tuple[int, int, int] = (230, 230, 230),  # Light gray
        border_color: tuple[int, int, int] = (100, 100, 100),  # Dark gray
        border_width: float = 0.5,
        style: dict | None = None,
    ):
        """
        Initialize score boxes.

        Args:
            current: Current score value (can be decimal like 2.5)
            total: Total possible score (number of boxes to show)
            box_width: Width of each box in mm
            box_height: Height of each box in mm
            spacing: Space between boxes in mm
            filled_color: RGB color for filled boxes
            empty_color: RGB color for empty boxes
            border_color: RGB color for box borders
            border_width: Width of box borders in mm
            style: Component styling
        """
        super().__init__(style)
        self.current = current
        self.total = total
        self.box_width = box_width
        self.box_height = box_height
        self.spacing = spacing
        self.filled_color = filled_color
        self.empty_color = empty_color
        self.border_color = border_color
        self.border_width = border_width

    def render(self, context: RenderContext) -> None:
        """Render the score boxes inline without moving to new line."""
        pdf = context.pdf
        start_x = pdf.get_x()
        start_y = pdf.get_y()

        # Calculate total width for all boxes (including spacing)
        total_width = (self.total * self.box_width) + ((self.total - 1) * self.spacing)

        # Step 1: Draw background rectangle (empty color for full total)
        pdf.set_fill_color(*self.empty_color)
        pdf.rect(x=start_x, y=start_y, w=total_width, h=self.box_height, style="F")

        # Step 2: Draw foreground rectangle (filled color for current score)
        # Calculate width based on current score
        current_width = (self.current * self.box_width) + ((self.current - 1) * self.spacing)
        if current_width > 0:
            pdf.set_fill_color(*self.filled_color)
            pdf.rect(x=start_x, y=start_y, w=current_width, h=self.box_height, style="F")

        # Step 3: Draw borders for each individual box
        pdf.set_draw_color(*self.border_color)
        pdf.set_line_width(self.border_width)
        for i in range(self.total):
            x_pos = start_x + (i * (self.box_width + self.spacing))
            pdf.rect(x=x_pos, y=start_y, w=self.box_width, h=self.box_height, style="D")

        # Move X position after the boxes (stay on same line)
        pdf.set_x(start_x + total_width)

    def __repr__(self) -> str:
        return f"ScoreBoxes(current={self.current}, total={self.total})"
