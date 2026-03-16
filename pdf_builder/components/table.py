"""Table component - renders tables with auto-layout."""

from pdf_builder.core import Component, Container, RenderContext
from pdf_builder.schemas import ColumnConfig, FontStyle


class Table(Component):
    """
    A table component for rendering tabular data.

    Features:
    - Auto-layout with column width calculation
    - Header styling
    - Row striping
    - Cell borders and colors
    - Text wrapping
    """

    def __init__(
        self,
        headers: list[str],
        data: list[list[str | Component]],
        col_widths: tuple[float, ...] | None = None,
        header_fill_color: tuple[int, int, int] | None = (200, 220, 255),
        header_text_color: tuple[int, int, int] = (0, 0, 0),
        row_fill_color: tuple[int, int, int] | None = (240, 240, 240),
        text_align: str | tuple[str, ...] = "L",
        width: float | None = None,
        font_size: int = 10,
        data_font_style: FontStyle = FontStyle.REGULAR,
        col_config: list[ColumnConfig] | None = None,
        style: dict | None = None,
    ):
        """
        Initialize a table.

        Args:
            headers: List of header labels
            data: List of rows (each row is a list of values - can be strings or Components)
            col_widths: Column width ratios (e.g., (1, 2, 1))
            header_fill_color: RGB color for header background
            header_text_color: RGB color for header text (default: black)
            row_fill_color: RGB color for alternating rows
            text_align: Text alignment - single value "L"/"C"/"R" for all columns,
                       or tuple ("L", "C", "R", ...) for per-column alignment
            width: Table width (None = full page width)
            font_size: Font size for table text (default: 10)
            data_font_style: Font style for data cells (REGULAR, BOLD, ITALIC, etc.)
            col_config: Optional list of ColumnConfig for advanced per-column configuration
            style: Additional styling
        """
        super().__init__(style)
        self.headers = headers
        self.data = data
        self.col_widths = col_widths
        self.header_fill_color = header_fill_color
        self.header_text_color = header_text_color
        self.row_fill_color = row_fill_color
        self.text_align = text_align
        self.width = width
        self.font_size = font_size
        self.data_font_style = data_font_style
        self.col_config = col_config

    def _has_components(self) -> bool:
        """Check if any cell contains a Component."""
        for row in self.data:
            for cell in row:
                if isinstance(cell, Component):
                    return True
        return False

    def _render_with_components(self, context: RenderContext) -> None:
        """Render table with support for Component cells (manual rendering)."""
        pdf = context.pdf
        font_family = pdf.font_family or "DejaVu"

        # Calculate table width
        table_width = self.width if self.width else context.get_page_width()

        # Calculate absolute column widths
        if self.col_widths:
            total_ratio = sum(self.col_widths)
            col_widths_abs = [
                (width / total_ratio) * table_width for width in self.col_widths
            ]
        else:
            # Distribute evenly
            col_width = table_width / len(self.headers)
            col_widths_abs = [col_width] * len(self.headers)

        # Determine text alignment for each column
        if self.col_config:
            alignments = [col.align for col in self.col_config]
        elif isinstance(self.text_align, tuple):
            alignments = list(self.text_align)
        else:
            alignments = [self.text_align] * len(self.headers)

        # Set border style
        pdf.set_line_width(0.1)
        pdf.set_draw_color(180, 180, 180)

        # Store starting position
        start_x = pdf.get_x()
        start_y = pdf.get_y()

        # Render header row
        if self.header_fill_color:
            pdf.set_fill_color(*self.header_fill_color)
            pdf.set_text_color(*self.header_text_color)
            pdf.set_font(font_family, style="B", size=self.font_size)

            current_x = start_x
            for i, (header, col_width, align) in enumerate(
                zip(self.headers, col_widths_abs, alignments)
            ):
                pdf.set_xy(current_x, start_y)
                pdf.multi_cell(
                    col_width,
                    self.font_size * 0.5,  # Cell height
                    header,
                    border=1,
                    align=align,
                    fill=True,
                )
                current_x += col_width

            start_y = pdf.get_y()

        # Reset text color and font for data rows
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_family, style=self.data_font_style, size=self.font_size)

        # Render data rows
        for data_row in self.data:
            # Calculate row height by checking all cells
            row_height = self._calculate_row_height(
                pdf, data_row, col_widths_abs, font_family
            )

            # Draw cell backgrounds if needed
            if self.row_fill_color:
                pdf.set_fill_color(*self.row_fill_color)
                current_x = start_x
                for col_width in col_widths_abs:
                    pdf.rect(current_x, start_y, col_width, row_height, "F")
                    current_x += col_width

            # Render cell content
            current_x = start_x
            for i, (cell_data, col_width, align) in enumerate(
                zip(data_row, col_widths_abs, alignments)
            ):
                # Draw cell border
                pdf.rect(current_x, start_y, col_width, row_height, "D")

                # Render cell content
                if isinstance(cell_data, Component):
                    # Save current position
                    cell_x = current_x + 1.5
                    cell_y = start_y + 1.5

                    # Set position for component
                    pdf.set_xy(cell_x, cell_y)

                    # Render Component (it will use current position)
                    cell_data.render(context)

                    # Note: Components may move the cursor, but we don't need to track it
                    # since we set absolute positions for each cell
                else:
                    # Render string
                    pdf.set_xy(current_x + 1.5, start_y + 1.5)  # Add padding
                    pdf.multi_cell(
                        col_width - 3,  # Account for padding
                        self.font_size * 0.4,
                        str(cell_data),
                        border=0,
                        align=align,
                        fill=False,
                    )

                current_x += col_width

            start_y += row_height

        # Reset styles
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)

        # Position cursor after table
        pdf.set_xy(start_x, start_y)
        pdf.ln(1)

    def _calculate_row_height(
        self, pdf, row_data: list, col_widths: list[float], font_family: str
    ) -> float:
        """Calculate the height needed for a row."""
        max_height = self.font_size * 0.5 * 2 + 3  # Minimum height with padding

        for cell_data, col_width in zip(row_data, col_widths):
            if isinstance(cell_data, Component):
                # For Components, estimate height (can be refined)
                # For now, use a default height
                cell_height = self.font_size * 2
            else:
                # For strings, calculate wrapped text height
                # Get number of lines needed
                text = str(cell_data)
                # Approximate: fpdf2 wraps based on character width
                char_width = pdf.get_string_width("x")
                chars_per_line = int((col_width - 3) / char_width)
                if chars_per_line > 0:
                    num_lines = len(text) // chars_per_line + (
                        1 if len(text) % chars_per_line else 0
                    )
                    num_lines = max(1, num_lines)
                else:
                    num_lines = 1
                cell_height = num_lines * self.font_size * 0.4 + 3

            max_height = max(max_height, cell_height)

        return max_height

    def render(self, context: RenderContext) -> None:
        """Render the table."""
        pdf = context.pdf

        # Set font size and style for table data cells
        pdf.set_font_size(self.font_size)
        # Store current font family for later use
        font_family = pdf.font_family or "DejaVu"

        # Reset fill color to white to avoid inheriting colors from previous elements
        pdf.set_fill_color(255, 255, 255)

        # Check if table contains any Components
        if self._has_components():
            # Use manual rendering for Component support
            self._render_with_components(context)
            return

        # Fast path: use fpdf2's table API for string-only tables
        # Calculate table width
        table_width = self.width if self.width else context.get_page_width()

        # Determine text alignment
        if self.col_config:
            # Use alignment from column configs
            text_align = tuple(col.align for col in self.col_config)
        else:
            # Use the text_align parameter (can be single value or tuple)
            text_align = self.text_align

        # Build table
        from fpdf.fonts import FontFace

        # Build table parameters
        table_params = {
            "width": table_width,
            "col_widths": self.col_widths,
            "text_align": text_align,
            "padding": 1.5,  # Reduced padding for more compact tables
        }

        # Set thinner border for table cells
        pdf.set_line_width(0.1)  # Very thin lines (0.1mm)
        pdf.set_draw_color(180, 180, 180)  # Light gray for borders

        # Add header styling if header fill color is set
        if self.header_fill_color:
            table_params["headings_style"] = FontFace(
                emphasis="BOLD",
                fill_color=self.header_fill_color,
                color=self.header_text_color,
            )

        # Add row fill color and mode only if row_fill_color is set
        if self.row_fill_color:
            # Custom fill mode to fill ALL cells (not just alternating rows)
            class AllCellsFillMode:
                @staticmethod
                def should_fill_cell(i, j):
                    return True  # Fill all cells

            table_params["cell_fill_color"] = self.row_fill_color
            table_params["cell_fill_mode"] = AllCellsFillMode()

        with pdf.table(**table_params) as table:
            # Add header row
            header_row = table.row()
            for header in self.headers:
                header_row.cell(header)

            # Set font style for data cells (not bold)
            pdf.set_font(font_family, style=self.data_font_style, size=self.font_size)

            # Add data rows
            for data_row in self.data:
                row = table.row()
                for cell_data in data_row:
                    row.cell(str(cell_data))

        # Reset line width and draw color to defaults
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0, 0, 0)  # Black

        # Add minimal spacing after table
        pdf.ln(1)

    def __repr__(self) -> str:
        return f"Table(cols={len(self.headers)}, rows={len(self.data)})"
