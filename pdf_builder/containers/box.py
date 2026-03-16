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
        height: float | None = None,
        spacing: float = 3,
        full_width: bool = False,
        vertical_align: str = "top",
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
            height: Box height (None = auto-calculated based on content)
            spacing: Spacing between children
            full_width: If True, temporarily set margins to 0 for full page width
            vertical_align: Vertical alignment of content ("top", "center", "bottom")
            style: Additional styling
        """
        super().__init__(children, layout="vertical", spacing=spacing, style=style)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.padding = padding
        self.width = width
        self.height = height
        self.full_width = full_width
        self.vertical_align = vertical_align

    def render(self, context: RenderContext) -> None:
        """
        Render the box with background and borders, then render children.
        Uses rectangle drawing for all modes (simpler and more consistent).
        """
        pdf = context.pdf

        # Save current margins
        saved_margins = (pdf.l_margin, pdf.r_margin)
        start_y = pdf.get_y()
        start_x = pdf.get_x()

        # Calculate box dimensions
        if self.full_width:
            # Temporarily set margins to 0 for full width
            pdf.set_margins(0, pdf.t_margin, 0)
            box_x = 0
            box_width = pdf.w
        else:
            box_x = start_x
            box_width = self.width if self.width else context.get_page_width()

        # Calculate content height
        if self.height:
            # Use explicit height if provided
            content_height = self.height
        else:
            # Auto-calculate (simplified - fixed height for now)
            # In a more advanced implementation, we'd pre-render children to measure
            content_height = self.padding * 2 + 10  # Approximate height

        # Draw background rectangle if color is set
        if self.background_color:
            pdf.set_fill_color(*self.background_color)
            pdf.rect(box_x, start_y, box_width, content_height, 'F')

        # Draw border if color is set
        if self.border_color:
            pdf.set_draw_color(*self.border_color)
            pdf.set_line_width(self.border_width)
            pdf.rect(box_x, start_y, box_width, content_height, 'D')

        # Calculate vertical position for content based on vertical_align
        if self.vertical_align == "center":
            # For center alignment, estimate content height and center it
            # Simplified: assume content is roughly one line of text (~5mm)
            estimated_content_height = 5  # mm
            vertical_offset = (content_height - estimated_content_height) / 2
            content_y = start_y + vertical_offset
        elif self.vertical_align == "bottom":
            # Position at bottom with padding
            content_y = start_y + content_height - self.padding - 5  # 5mm estimated content height
        else:
            # Default: top alignment with padding
            content_y = start_y + self.padding

        # Position cursor for content rendering
        pdf.set_y(content_y)
        pdf.set_x(box_x + self.padding)

        # Adjust margins for content area
        if self.full_width:
            pdf.set_margins(self.padding, pdf.t_margin, self.padding)
        else:
            # Keep original margins but account for box position
            pdf.set_margins(box_x + self.padding, pdf.t_margin, saved_margins[1])

        # Render children
        for i, child in enumerate(self.children):
            child.render(context)
            if i < len(self.children) - 1 and self.spacing > 0:
                pdf.ln(self.spacing)

        # Move past the box
        pdf.set_y(start_y + content_height)

        # Restore original margins
        pdf.set_margins(saved_margins[0], pdf.t_margin, saved_margins[1])

    def _render_background(self, context: RenderContext) -> None:
        """Render box background and border."""
        # Handled by table rendering in render() method
        pass

    def __repr__(self) -> str:
        return f"Box(bg={self.background_color}, border={self.border_color}, children={len(self.children)})"
