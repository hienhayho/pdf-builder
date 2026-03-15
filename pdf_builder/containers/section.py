"""Section container - logical grouping of content."""

from pdf_builder.core import Container, RenderContext


class Section(Container):
    """
    A section container for grouping related content.

    Sections help organize content logically and can have:
    - Titles
    - Numbering
    - Consistent spacing
    - Optional backgrounds
    """

    def __init__(
        self,
        children: list | None = None,
        title: str | None = None,
        numbering: str | None = None,
        spacing: float = 8,
        style: dict | None = None,
    ):
        """
        Initialize a section.

        Args:
            children: Child components
            title: Section title (optional)
            numbering: Section number/label (e.g., "3.1", "A", etc.)
            spacing: Spacing between children
            style: Section styling
        """
        super().__init__(children, layout="vertical", spacing=spacing, style=style)
        self.title = title
        self.numbering = numbering

    def render(self, context: RenderContext) -> None:
        """
        Render the section.

        If title is provided, render it first, then children.
        """
        pdf = context.pdf

        # Render section title if provided
        if self.title:
            # Save current font
            current_font = pdf.font_family
            current_size = pdf.font_size_pt
            current_style = pdf.font_style

            # Render title
            title_text = f"{self.numbering}. {self.title}" if self.numbering else self.title
            pdf.set_font(current_font, "B", current_size + 2)
            pdf.cell(0, 10, title_text, ln=True)
            pdf.ln(3)

            # Restore font
            pdf.set_font(current_font, current_style, current_size)

        # Render children
        super().render(context)

    def __repr__(self) -> str:
        title_str = f"title='{self.title}'" if self.title else ""
        return f"Section({title_str}, children={len(self.children)})"
