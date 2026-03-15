"""Box container - colored boxes with borders and padding."""

from fpdf.enums import Align

from pdf_builder.core import Container, RenderContext


class Box(Container):
    """
    A box container with background color, borders, and padding.

    Perfect for:
    - Colored header boxes
    - Highlighted sections
    - Card-like components
    """

    def __init__(
        self,
        children: list | None = None,
        background_color: tuple[int, int, int] | None = None,
        border_color: tuple[int, int, int] | None = None,
        border_width: float = 0.5,
        padding: float = 5,
        width: float | None = None,
        spacing: float = 3,
        full_width: bool = False,
        style: dict | None = None,
    ):
        """
        Initialize a box container.

        Args:
            children: Child components
            background_color: RGB tuple (e.g., (255, 102, 0) for orange)
            border_color: RGB tuple for border
            border_width: Border width in mm
            padding: Internal padding in mm
            width: Box width (None = full page width)
            spacing: Spacing between children
            full_width: If True, temporarily set margins to 0 for full page width
            style: Additional styling
        """
        super().__init__(children, layout="vertical", spacing=spacing, style=style)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.padding = padding
        self.width = width
        self.full_width = full_width

    def render(self, context: RenderContext) -> None:
        """
        Render the box with background and borders, then render children.
        """
        pdf = context.pdf

        # Save current margins if full_width is enabled
        saved_margins = None
        if self.full_width:
            saved_margins = (pdf.l_margin, pdf.r_margin)
            pdf.set_margins(0, pdf.t_margin, 0)
            pdf.set_x(0)  # Reset X position to left edge

        # Calculate box width
        if self.full_width:
            box_width = pdf.w  # Full page width
        else:
            box_width = self.width if self.width else context.get_page_width()

        # Save current position
        start_y = pdf.get_y()
        start_x = pdf.get_x()

        # Render children first to calculate height (in memory)
        # For simplicity, we'll use a table with single cell
        table_params = {
            "width": box_width,
            "padding": self.padding,
            "align": Align.L,
            "borders_layout": "NONE",  # Disable default table borders
        }

        # Only add fill parameters if background color is set
        if self.background_color:
            table_params["cell_fill_color"] = self.background_color
            table_params["cell_fill_mode"] = "ALL"

        with pdf.table(**table_params) as table:
            row = table.row()
            cell = row.cell()

            # Render children inside the cell
            # Note: This is a simplified approach
            # For more complex layouts, we'd need to render to a sub-context
            for i, child in enumerate(self.children):
                child.render(context)
                if i < len(self.children) - 1 and self.spacing > 0:
                    pdf.ln(self.spacing)

        # Restore margins if they were changed
        if saved_margins:
            pdf.set_margins(saved_margins[0], pdf.t_margin, saved_margins[1])

    def _render_background(self, context: RenderContext) -> None:
        """Render box background and border."""
        # Handled by table rendering in render() method
        pass

    def __repr__(self) -> str:
        return f"Box(bg={self.background_color}, border={self.border_color}, children={len(self.children)})"
