"""Link component - render clickable hyperlinks in PDFs."""

from pdf_builder.core import Component, RenderContext


class Link(Component):
    """
    Render a clickable hyperlink in the PDF.

    The link text can be different from the URL.

    Example:
        Link(text="Click here", url="https://example.com")
        Link(text="Link", url="https://example.com", color=(0, 0, 255))
    """

    def __init__(
        self,
        text: str,
        url: str,
        font_size: int = 11,
        color: tuple[int, int, int] = (0, 0, 255),  # Blue by default
        underline: bool = True,
        new_line: bool = True,
        style: dict | None = None,
    ):
        """
        Initialize link component.

        Args:
            text: Display text for the link
            url: URL to link to
            font_size: Font size for the link text
            color: RGB color for the link (default: blue)
            underline: Whether to underline the link (default: True)
            new_line: Whether to move to new line after rendering (default: True)
            style: Component styling
        """
        super().__init__(style)
        self.text = text
        self.url = url
        self.font_size = font_size
        self.color = color
        self.underline = underline
        self.new_line = new_line

    def render(self, context: RenderContext) -> None:
        """Render the clickable link inline."""
        pdf = context.pdf

        # Set link color
        pdf.set_text_color(*self.color)

        # Set font style (with underline if enabled)
        font_style = "U" if self.underline else ""
        pdf.set_font(pdf.font_family or "Arial", style=font_style, size=self.font_size)

        # Calculate line height
        line_height = self.font_size * 0.5

        # Render the link using write() for inline rendering
        # The link parameter makes it clickable
        pdf.write(h=line_height, text=self.text, link=self.url)

        # Move to new line if enabled
        if self.new_line:
            pdf.ln()

        # Reset font style and color
        pdf.set_font(pdf.font_family or "Arial", style="", size=self.font_size)
        pdf.set_text_color(0, 0, 0)

    def __repr__(self) -> str:
        return f"Link(text='{self.text}', url='{self.url}')"
