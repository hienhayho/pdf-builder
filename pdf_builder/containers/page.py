"""Page container - represents a PDF page."""

from pdf_builder.containers.footer import Footer
from pdf_builder.core import Container, RenderContext


class Page(Container):
    """
    Represents a page in the PDF document.

    A page is the top-level container that holds all content.
    It manages page breaks and overall page layout.
    """

    def __init__(
        self,
        children: list | None = None,
        orientation: str = "portrait",
        spacing: float = 5,
        style: dict | None = None,
    ):
        """
        Initialize a page.

        Args:
            children: Child components
            orientation: Page orientation - "portrait" or "landscape"
            spacing: Default spacing between elements (in mm)
            style: Page styling (margins, background, etc.)
        """
        super().__init__(children, layout="vertical", spacing=spacing, style=style)
        self.orientation = orientation

    def render(self, context: RenderContext) -> None:
        """
        Render the page and all its children.

        Adds a new page to the PDF before rendering children.
        Footer children are handled specially to ensure they render at the bottom.
        """
        pdf = context.pdf

        # Add a new page
        pdf.add_page(orientation=self.orientation[0].upper())

        # Store the page number where this Page starts
        page_number = pdf.page

        # Separate Footer children from regular children
        footer_children = [c for c in self.children if isinstance(c, Footer)]
        non_footer_children = [c for c in self.children if not isinstance(c, Footer)]

        # If we have footers, reserve space for them by adjusting auto page break margin
        if footer_children:
            # Calculate maximum space needed for footers
            max_footer_space = max(f.margin_bottom + 20 for f in footer_children)  # +20mm for content height

            # Save original bottom margin and adjust it
            original_b_margin = pdf.b_margin
            pdf.set_auto_page_break(auto=True, margin=max_footer_space)

        # Render non-footer children with spacing
        for i, child in enumerate(non_footer_children):
            child.render(context)
            if i < len(non_footer_children) - 1 and self.spacing > 0:
                pdf.ln(self.spacing)

        # Restore original auto page break margin
        if footer_children:
            pdf.set_auto_page_break(auto=True, margin=original_b_margin)

        # Render footer children at their absolute positions on the original page
        # Pass the page number to the footer
        for footer in footer_children:
            context.set('footer_page_number', page_number)
            footer.render(context)

    def __repr__(self) -> str:
        return f"Page(orientation={self.orientation}, children={len(self.children)})"
