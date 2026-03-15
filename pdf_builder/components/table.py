"""Table component - renders tables with auto-layout."""

from fpdf.enums import Align, TableCellFillMode

from pdf_builder.core import Component, RenderContext


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
        data: list[list[str]],
        col_widths: tuple[float, ...] | None = None,
        header_fill_color: tuple[int, int, int] | None = (200, 220, 255),
        row_fill_color: tuple[int, int, int] | None = (240, 240, 240),
        text_align: str = "L",
        width: float | None = None,
        style: dict | None = None,
    ):
        """
        Initialize a table.

        Args:
            headers: List of header labels
            data: List of rows (each row is a list of values)
            col_widths: Column width ratios (e.g., (1, 2, 1))
            header_fill_color: RGB color for header background
            row_fill_color: RGB color for alternating rows
            text_align: Text alignment in cells
            width: Table width (None = full page width)
            style: Additional styling
        """
        super().__init__(style)
        self.headers = headers
        self.data = data
        self.col_widths = col_widths
        self.header_fill_color = header_fill_color
        self.row_fill_color = row_fill_color
        self.text_align = text_align
        self.width = width

    def render(self, context: RenderContext) -> None:
        """Render the table."""
        pdf = context.pdf

        # Calculate table width
        table_width = self.width if self.width else context.get_page_width()

        # Build table
        from fpdf.fonts import FontFace

        with pdf.table(
            width=table_width,
            col_widths=self.col_widths,
            headings_style=FontFace(
                emphasis="BOLD", fill_color=self.header_fill_color
            )
            if self.header_fill_color
            else None,
            cell_fill_color=self.row_fill_color,
            cell_fill_mode=TableCellFillMode.ROWS if self.row_fill_color else None,
            text_align=self.text_align,
            padding=3,
        ) as table:
            # Add header row
            header_row = table.row()
            for header in self.headers:
                header_row.cell(header)

            # Add data rows
            for data_row in self.data:
                row = table.row()
                for cell_data in data_row:
                    row.cell(str(cell_data))

        # Add spacing after table
        pdf.ln(5)

    def __repr__(self) -> str:
        return f"Table(cols={len(self.headers)}, rows={len(self.data)})"
