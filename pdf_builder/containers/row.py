"""Row container - horizontal layout."""

from enum import Enum

from pdf_builder.core import Container, RenderContext


class RowJustify(Enum):
    """Justification options for Row layout (similar to CSS flexbox)."""

    FLEX_START = "flex-start"  # Align to the start (left)
    FLEX_END = "flex-end"  # Align to the end (right)
    CENTER = "center"  # Center items
    SPACE_BETWEEN = "space-between"  # Space between items
    SPACE_AROUND = "space-around"  # Space around items


class Row(Container):
    """
    A row container that lays out children horizontally.

    Useful for:
    - Multi-column layouts
    - Side-by-side elements
    - Grid systems
    - Flex-like layouts

    Supports flex-like properties:
    - justify: "space-between", "space-around", "flex-start", "flex-end", "center"
    """

    def __init__(
        self,
        children: list | None = None,
        column_widths: list[float] | None = None,
        spacing: float = 5,
        justify: RowJustify | str = RowJustify.FLEX_START,
        style: dict | None = None,
    ):
        """
        Initialize a row container.

        Args:
            children: Child components
            column_widths: Width ratios for each column (e.g., [1, 2, 1])
            spacing: Horizontal spacing between columns
            justify: Horizontal alignment (RowJustify enum or string: "space-between", "flex-start", etc.)
            style: Row styling
        """
        super().__init__(children, layout="horizontal", spacing=spacing, style=style)
        self.column_widths = column_widths
        # Support both Enum and string for backward compatibility
        if isinstance(justify, RowJustify):
            self.justify = justify.value
        else:
            self.justify = justify

    def render(self, context: RenderContext) -> None:
        """
        Render children horizontally with flex-like justification.
        """
        pdf = context.pdf
        page_width = context.get_page_width()
        num_cols = len(self.children)
        start_y = pdf.get_y()

        if num_cols == 0:
            return

        # Handle justify="space-between" - special case for footer-like layouts
        if self.justify == RowJustify.SPACE_BETWEEN.value and num_cols == 2:
            from pdf_builder.components.text import Text

            # Helper function to extract texts from child
            def get_texts(child):
                """Get list of Text components from child (Text or Row)."""
                if isinstance(child, Text):
                    return [child]
                elif isinstance(child, Row):
                    return [t for t in child.children if isinstance(t, Text)]
                return []

            # Get all text components
            left_texts = get_texts(self.children[0])
            right_texts = get_texts(self.children[1])

            if not left_texts or not right_texts:
                return

            # Calculate total widths for both sides
            left_total_width = 0
            for text in left_texts:
                pdf.set_font(pdf.font_family or "Arial", text.font_style, text.font_size)
                content = text.get_rendered_content(context)
                left_total_width += pdf.get_string_width(content)

            right_total_width = 0
            for text in right_texts:
                pdf.set_font(pdf.font_family or "Arial", text.font_style, text.font_size)
                content = text.get_rendered_content(context)
                right_total_width += pdf.get_string_width(content)

            # Get line height from first text
            line_height = left_texts[0].line_height if left_texts else 10

            # Save Y position to ensure both sides are on the same line
            start_y = pdf.get_y()

            # Render left texts using cell() with ln=0
            for i, text in enumerate(left_texts):
                content = text.get_rendered_content(context)
                pdf.set_font(pdf.font_family or "Arial", text.font_style, text.font_size)
                pdf.set_text_color(*text.color)
                text_width = pdf.get_string_width(content)
                pdf.cell(w=text_width, h=line_height, txt=content, ln=0)
                pdf.set_text_color(0, 0, 0)

            # For space-between, always position right text at the right edge
            # Go back to the same Y position and set X to right edge
            pdf.set_y(start_y)
            right_x = pdf.w - pdf.r_margin - right_total_width
            pdf.set_x(right_x)

            # Render right texts using cell()
            for i, text in enumerate(right_texts):
                content = text.get_rendered_content(context)
                pdf.set_font(pdf.font_family or "Arial", text.font_style, text.font_size)
                pdf.set_text_color(*text.color)
                text_width = pdf.get_string_width(content)
                # Last text moves to next line
                ln = 1 if i == len(right_texts) - 1 else 0
                pdf.cell(w=text_width, h=line_height, txt=content, ln=ln)
                pdf.set_text_color(0, 0, 0)

        else:
            # Default layout with column widths
            if not self.column_widths:
                self.column_widths = [1] * num_cols

            total_ratio = sum(self.column_widths)
            actual_widths = [
                (ratio / total_ratio) * page_width for ratio in self.column_widths
            ]

            # Use table for horizontal layout
            with pdf.table(
                col_widths=tuple(actual_widths),
                borders_layout="NONE",
            ) as table:
                row = table.row()
                for i, child in enumerate(self.children):
                    cell = row.cell()
                    child.render(context)

    def __repr__(self) -> str:
        return f"Row(columns={len(self.children)}, widths={self.column_widths})"
