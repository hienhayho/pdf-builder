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
        start_y = pdf.get_y()  # Get current Y (might be centered by parent Box)
        start_x = pdf.get_x()  # Get current X

        if num_cols == 0:
            return

        # Handle justify="space-between" - special case for footer-like layouts
        if self.justify == RowJustify.SPACE_BETWEEN.value and num_cols == 2:
            from pdf_builder.components.text import Text
            from pdf_builder.components.image import Image

            # Render left child at left margin
            left_child = self.children[0]
            pdf.set_xy(pdf.l_margin, start_y)

            # Track text height for vertical alignment
            text_height = 0

            if isinstance(left_child, Text):
                # Render text using cell() for inline rendering
                content = left_child.get_rendered_content(context)
                pdf.set_font(pdf.font_family or "Arial", left_child.font_style, left_child.font_size)
                pdf.set_text_color(*left_child.color)
                text_width = pdf.get_string_width(content)
                text_height = left_child.line_height
                pdf.cell(w=text_width, h=text_height, txt=content, ln=0)
                pdf.set_text_color(0, 0, 0)
            elif isinstance(left_child, Row):
                # For nested Row, render children inline
                for child in left_child.children:
                    if isinstance(child, Text):
                        content = child.get_rendered_content(context)
                        pdf.set_font(pdf.font_family or "Arial", child.font_style, child.font_size)
                        pdf.set_text_color(*child.color)
                        text_width = pdf.get_string_width(content)
                        text_height = max(text_height, child.line_height)  # Track max height
                        pdf.cell(w=text_width, h=child.line_height, txt=content, ln=0)
                        pdf.set_text_color(0, 0, 0)
                    else:
                        child.render(context)
            else:
                left_child.render(context)
                # Estimate text height if not already set
                if text_height == 0:
                    text_height = 5  # Default estimate

            # Get the Y position after left child
            end_y_left = pdf.get_y()

            # Calculate right child width and render at right edge
            right_child = self.children[1]

            # Estimate width of right child
            right_width = 0
            if isinstance(right_child, Text):
                pdf.set_font(pdf.font_family or "Arial", right_child.font_style, right_child.font_size)
                content = right_child.get_rendered_content(context)
                right_width = pdf.get_string_width(content)
            elif isinstance(right_child, Image):
                # Use image width
                right_width = right_child.width if right_child.width else 20
            elif isinstance(right_child, Row):
                # For nested Row, sum widths of children
                for child in right_child.children:
                    if isinstance(child, Text):
                        pdf.set_font(pdf.font_family or "Arial", child.font_style, child.font_size)
                        content = child.get_rendered_content(context)
                        right_width += pdf.get_string_width(content)
                    elif isinstance(child, Image):
                        right_width += child.width if child.width else 20

            # Position at right edge and render
            pdf.set_y(start_y)
            right_x = pdf.w - pdf.r_margin - right_width
            pdf.set_x(right_x)

            if isinstance(right_child, Text):
                # Render text using cell() for inline rendering
                content = right_child.get_rendered_content(context)
                pdf.set_font(pdf.font_family or "Arial", right_child.font_style, right_child.font_size)
                pdf.set_text_color(*right_child.color)
                text_width = pdf.get_string_width(content)
                pdf.cell(w=text_width, h=right_child.line_height, txt=content, ln=0)
                pdf.set_text_color(0, 0, 0)
            elif isinstance(right_child, Image):
                # For Image, render directly at current position without ln()
                from PIL import Image as PILImage
                img = PILImage.open(right_child.path)
                img_width_px, img_height_px = img.size

                # Calculate dimensions
                if right_child.width and right_child.keep_aspect_ratio:
                    aspect_ratio = img_height_px / img_width_px
                    calculated_height = right_child.width * aspect_ratio
                else:
                    calculated_height = right_child.height if right_child.height else img_height_px * 25.4 / 96

                # Center image vertically relative to text
                # If text_height is known, align image center with text center
                if text_height > 0:
                    # Calculate Y to center image relative to text
                    image_y = start_y + (text_height - calculated_height) / 2
                else:
                    image_y = start_y

                # Render image at calculated position
                pdf.image(
                    right_child.path,
                    x=right_x,  # Use the calculated right position
                    y=image_y,  # Vertically centered with text
                    w=right_child.width,
                    h=calculated_height,
                    keep_aspect_ratio=right_child.keep_aspect_ratio,
                )
            elif isinstance(right_child, Row):
                # For nested Row, render children inline
                for child in right_child.children:
                    if isinstance(child, Text):
                        content = child.get_rendered_content(context)
                        pdf.set_font(pdf.font_family or "Arial", child.font_style, child.font_size)
                        pdf.set_text_color(*child.color)
                        text_width = pdf.get_string_width(content)
                        pdf.cell(w=text_width, h=child.line_height, txt=content, ln=0)
                        pdf.set_text_color(0, 0, 0)
                    else:
                        child.render(context)
            else:
                right_child.render(context)

            # Move to next line after the row
            pdf.ln()  # Move to next line

            return
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
