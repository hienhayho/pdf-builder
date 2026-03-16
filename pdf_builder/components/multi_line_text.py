"""Multi-line text component with explicit line breaks."""

from pdf_builder.core import Component, RenderContext
from pdf_builder.schemas import FontStyle, MultiLineItem


class MultiLineText(Component):
    """
    Multi-line text component that renders multiple lines of text as a cohesive unit.

    Unlike Text which uses multi_cell for automatic wrapping, MultiLineText allows
    you to explicitly specify line breaks for precise control over text layout.
    Useful for titles, headers, or any content where you want specific line breaks.

    Each line can have its own styling (font_size, font_style, color) using MultiLineItem,
    or you can pass simple strings which will inherit the default styling.

    Args:
        lines: List of text strings OR MultiLineItem objects with individual styling
        font_size: Default font size in points (default: 10)
        font_style: Default font style - REGULAR, BOLD, ITALIC, BOLD_ITALIC
        color: Default RGB tuple (r, g, b) where each value is 0-255
        align: Text alignment - "L" (left), "C" (center), "R" (right)
        line_height: Multiplier for line spacing (default: 1.2)
        style: Additional style dictionary

    Example with simple strings:
        >>> title = MultiLineText(
        ...     lines=[
        ...         "CHƯƠNG TRÌNH ĐÀO TẠO TRƯỞNG PHÒNG KINH DOANH",
        ...         "KHU VỰC MIỀN TRUNG TÂY NGUYÊN",
        ...     ],
        ...     font_size=14,
        ...     font_style=FontStyle.BOLD,
        ...     color=(255, 102, 0),
        ...     align="C"
        ... )

    Example with MultiLineItem for individual styling:
        >>> from pdf_builder.schemas import MultiLineItem, FontStyle
        >>> title = MultiLineText(
        ...     lines=[
        ...         MultiLineItem(
        ...             text="CHƯƠNG TRÌNH ĐÀO TẠO",
        ...             font_size=16,
        ...             font_style=FontStyle.BOLD
        ...         ),
        ...         MultiLineItem(
        ...             text="Năm 2026",
        ...             font_size=14,
        ...             font_style=FontStyle.BOLD_ITALIC,
        ...             color=(255, 102, 0)
        ...         ),
        ...     ],
        ...     align="C"
        ... )
    """

    def __init__(
        self,
        lines: list[str] | list[MultiLineItem],
        font_size: int = 10,
        font_style: FontStyle | str = FontStyle.REGULAR,
        color: tuple[int, int, int] | None = None,
        align: str = "L",
        line_height: float = 1.2,
        style: dict | None = None,
    ):
        super().__init__(style)

        # Convert strings to MultiLineItem objects if needed
        self.items: list[MultiLineItem] = []
        for line in lines:
            if isinstance(line, str):
                self.items.append(MultiLineItem(text=line))
            else:
                self.items.append(line)

        self.default_font_size = font_size
        self.default_font_style = font_style.value if isinstance(font_style, FontStyle) else font_style
        self.default_color = color if color is not None else (0, 0, 0)
        self.align = align
        self.line_height = line_height

    def render(self, context: RenderContext) -> None:
        """
        Render multiple lines of text with explicit line breaks.

        Each line can have its own styling (font_size, font_style, color) or inherit
        from the default values.

        Args:
            context: Rendering context containing the PDF instance
        """
        pdf = context.pdf

        # Render each line with its individual styling
        for item in self.items:
            # Determine styling for this line (use item's values or fall back to defaults)
            line_font_size = item.font_size if item.font_size is not None else self.default_font_size
            line_font_style = item.font_style if item.font_style is not None else self.default_font_style
            line_color = item.color if item.color is not None else self.default_color

            # Set font and color for this line
            pdf.set_font("DejaVu", line_font_style, line_font_size)
            pdf.set_text_color(*line_color)

            # Calculate line height in mm for this line
            line_height_mm = line_font_size * self.line_height * 0.352778  # points to mm

            # Skip empty lines but still add spacing
            if not item.text:
                pdf.ln(line_height_mm)
                continue

            # Get current Y position
            y = pdf.get_y()

            # For center and right alignment, calculate exact position
            # For left alignment, use built-in cell alignment
            if self.align == "C":
                # Center alignment - calculate exact x position
                page_width = context.get_page_width()
                text_width = pdf.get_string_width(item.text)
                x = (page_width - text_width) / 2 + pdf.l_margin
                pdf.set_xy(x, y)
                pdf.cell(text_width, line_height_mm, item.text)
            elif self.align == "R":
                # Right alignment - calculate exact x position
                page_width = context.get_page_width()
                text_width = pdf.get_string_width(item.text)
                x = page_width - text_width - pdf.r_margin
                pdf.set_xy(x, y)
                pdf.cell(text_width, line_height_mm, item.text)
            else:
                # Left alignment - use cell's built-in alignment
                pdf.cell(0, line_height_mm, item.text, align="L")

            # Move to next line
            pdf.ln(line_height_mm)

        # Reset text color to black
        pdf.set_text_color(0, 0, 0)
