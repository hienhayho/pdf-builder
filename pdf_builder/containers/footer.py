"""Footer container - fixed position footer at bottom of page."""

from pdf_builder.core import Container, RenderContext


class Footer(Container):
    """
    A footer container that positions itself at the bottom of the page.

    Perfect for:
    - Page footers with metadata
    - Copyright information
    - Page numbers
    - Author/date information
    """

    def __init__(
        self,
        children: list | None = None,
        margin_bottom: float = 15,
        spacing: float = 0,
        style: dict | None = None,
    ):
        """
        Initialize a footer container.

        Args:
            children: Child components (typically Row or Text)
            margin_bottom: Distance from bottom of page in mm
            spacing: Spacing between children
            style: Additional styling
        """
        super().__init__(children, layout="vertical", spacing=spacing, style=style)
        self.margin_bottom = margin_bottom

    def render(self, context: RenderContext) -> None:
        """
        Render footer at fixed position at bottom of page.
        """
        pdf = context.pdf

        # Get the target page number from context (set by Page container)
        target_page = context.get('footer_page_number', pdf.page)

        # Save current page
        current_page = pdf.page

        # Go to the target page if we're not already there
        if current_page != target_page:
            pdf.page = target_page

        # Calculate footer position from bottom
        page_height = pdf.h  # Total page height
        footer_y = page_height - self.margin_bottom

        # Disable automatic page breaks while rendering footer
        # This prevents fpdf2 from triggering page breaks when we render at the bottom
        pdf.set_auto_page_break(auto=False)

        # Move to footer position
        pdf.set_y(footer_y)

        # Render all children
        for i, child in enumerate(self.children):
            child.render(context)
            if i < len(self.children) - 1 and self.spacing > 0:
                pdf.ln(self.spacing)

        # Re-enable automatic page breaks
        pdf.set_auto_page_break(auto=True)

        # Restore the page back to where we were if we changed it
        if current_page != target_page:
            pdf.page = current_page

    def __repr__(self) -> str:
        return f"Footer(children={len(self.children)}, margin_bottom={self.margin_bottom}mm)"
