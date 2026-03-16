"""InlineText component - render text with mixed styles on the same line."""

from pdf_builder.core import Component, RenderContext
from pdf_builder.schemas import InlineSegment


class InlineText(Component):
    """
    Render multiple text segments with different styles on the same line.

    Useful for combining bold, italic, and regular text inline with automatic text wrapping.

    Example:
        from pdf_builder import InlineText, InlineSegment, FontStyle

        InlineText([
            InlineSegment(text="Bold text: ", style=FontStyle.BOLD),
            InlineSegment(text="Red italic text", style=FontStyle.ITALIC, color=(255, 0, 0)),
        ])
    """

    def __init__(
        self,
        segments: list[InlineSegment],
        font_size: int = 11,
        align: str = "L",
        new_line: bool = True,
        style: dict | None = None,
    ):
        """
        Initialize inline text with multiple styled segments.

        Args:
            segments: List of InlineSegment objects defining text, style, and color
            font_size: Font size for all segments
            align: Text alignment (not used for inline segments)
            new_line: Whether to move to new line after rendering (default: True)
            style: Component styling
        """
        super().__init__(style)
        self.segments = segments
        self.font_size = font_size
        self.align = align
        self.new_line = new_line

    def render(self, context: RenderContext) -> None:
        """Render all segments on the same line with different styles and automatic wrapping."""
        pdf = context.pdf

        # Calculate line height based on font size
        line_height = self.font_size * 0.5  # Approximate line height in mm

        # Render each segment with its own style using write() for text wrapping
        for segment in self.segments:
            # Replace template placeholders if data is provided
            text = segment.text
            if context.data:
                import re

                def replace_placeholder(match):
                    field_name = match.group(1)
                    if hasattr(context.data, field_name):
                        value = getattr(context.data, field_name)
                        # Handle date formatting
                        if hasattr(value, "strftime"):
                            return value.strftime("%d.%m.%Y")
                        return str(value)
                    return match.group(0)  # Keep original if field not found

                text = re.sub(r"\{\{(\w+)\}\}", replace_placeholder, text)

            # Set the style and color for this segment
            pdf.set_font(
                pdf.font_family or "Arial",
                style=segment.style,
                size=self.font_size,
            )
            pdf.set_text_color(*segment.color)

            # Use write() for automatic text wrapping and flowing text
            pdf.write(h=line_height, text=text)

        # Move to next line after all segments (if enabled)
        if self.new_line:
            pdf.ln()

        # Reset to regular style and color
        pdf.set_font(pdf.font_family or "Arial", style="", size=self.font_size)
        pdf.set_text_color(0, 0, 0)

    def get_placeholders(self) -> set[str]:
        """
        Extract all {{placeholder}} names from all segments.

        Returns:
            Set of placeholder names found in the text segments
        """
        import re

        placeholders = set()
        pattern = r"\{\{(\w+)\}\}"

        for segment in self.segments:
            matches = re.findall(pattern, segment.text)
            placeholders.update(matches)

        return placeholders

    def __repr__(self) -> str:
        return f"InlineText(segments={len(self.segments)})"
