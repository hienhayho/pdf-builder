"""Main Document class - the entry point for creating PDFs."""

from pathlib import Path

from fpdf import FPDF
from pydantic import BaseModel

from .components.text import Text
from .core import Container, RenderContext
from .containers import Page


class Document:
    """
    The main document class - the root of the component tree.

    A Document contains Pages, which contain Containers and Components.

    Example:
        >>> doc = Document()
        >>> page = Page()
        >>> page.add(Heading("Hello World"))
        >>> doc.add(page)
        >>> doc.render("output.pdf")
    """

    def __init__(
        self,
        title: str = "",
        author: str = "",
        font_family: str = "Arial",
        font_size: float = 11,
        unicode_support: bool = False,
        font_path: str | None = None,
        margin_left: float = 10,
        margin_top: float = 10,
        margin_right: float = 10,
    ):
        """
        Initialize a document.

        Args:
            title: Document title (PDF metadata)
            author: Document author (PDF metadata)
            font_family: Default font family (ignored if unicode_support=True)
            font_size: Default font size
            unicode_support: Enable Unicode font support (uses DejaVu fonts)
            font_path: Path to custom TTF font file for Unicode support
            margin_left: Left page margin in mm (default: 10)
            margin_top: Top page margin in mm (default: 10)
            margin_right: Right page margin in mm (default: 10)
        """
        self.title = title
        self.author = author
        self.font_family = font_family
        self.font_size = font_size
        self.unicode_support = unicode_support
        self.font_path = font_path
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.margin_right = margin_right
        self.pages: list[Page] = []

    def add(self, *pages: Page) -> "Document":
        """
        Add one or more pages to the document.

        Args:
            *pages: Page objects to add

        Returns:
            Self for method chaining
        """
        self.pages.extend(pages)
        return self

    def get_required_fields(self) -> set[str]:
        """
        Get all template field names required by this document.

        Walks the component tree to find all {{field_name}} placeholders
        in Text components.

        Returns:
            Set of field names that need to be provided in the data model
        """
        fields = set()

        def collect_fields(component):
            """Recursively collect fields from component tree."""
            if isinstance(component, Text):
                fields.update(component.get_placeholders())
            if isinstance(component, Container):
                for child in component.children:
                    collect_fields(child)

        # Collect from all pages
        for page in self.pages:
            collect_fields(page)

        return fields

    def render(self, output_path: str, data: BaseModel | None = None) -> None:
        """
        Render the document to a PDF file.

        Args:
            output_path: Path where the PDF will be saved
            data: Optional Pydantic model containing dynamic data for the document
                  (e.g., employee info, dates, company details)
        """
        # Create PDF instance
        pdf = FPDF()

        # Set page margins
        pdf.set_margins(self.margin_left, self.margin_top, self.margin_right)

        # Set metadata
        if self.title:
            pdf.set_title(self.title)
        if self.author:
            pdf.set_author(self.author)

        # Add Unicode font support if enabled
        if self.unicode_support:
            # Enable text shaping for complex scripts
            pdf.set_text_shaping(True)

            # Try to find and add DejaVu fonts
            if self.font_path:
                # Use custom font path
                pdf.add_font(family="DejaVu", fname=self.font_path)

                # Try to find bold variant
                bold_path = self.font_path.replace(".ttf", "-Bold.ttf")
                if Path(bold_path).exists():
                    pdf.add_font(family="DejaVu", style="B", fname=bold_path)

                # Try to find italic variant
                italic_path = self.font_path.replace(".ttf", "-Oblique.ttf")
                if Path(italic_path).exists():
                    pdf.add_font(family="DejaVu", style="I", fname=italic_path)

                # Try to find bold-italic variant
                bold_italic_path = self.font_path.replace(".ttf", "-BoldOblique.ttf")
                if Path(bold_italic_path).exists():
                    pdf.add_font(family="DejaVu", style="BI", fname=bold_italic_path)
            else:
                # Use project root fonts
                project_root = Path(__file__).parent.parent
                font_path = project_root / "assets" / "fonts" / "DejaVuSans.ttf"

                if not font_path.exists():
                    raise FileNotFoundError(
                        f"DejaVu font not found at {font_path}. "
                        f"Please add the font to assets/fonts/ or provide font_path parameter."
                    )

                # Add regular font
                pdf.add_font(family="DejaVu", fname=str(font_path))

                # Try to add bold variant
                bold_path = font_path.parent / "DejaVuSans-Bold.ttf"
                if bold_path.exists():
                    pdf.add_font(family="DejaVu", style="B", fname=str(bold_path))

                # Try to add italic variant
                italic_path = font_path.parent / "DejaVuSans-Oblique.ttf"
                if italic_path.exists():
                    pdf.add_font(family="DejaVu", style="I", fname=str(italic_path))

                # Try to add bold-italic variant
                bold_italic_path = font_path.parent / "DejaVuSans-BoldOblique.ttf"
                if bold_italic_path.exists():
                    pdf.add_font(family="DejaVu", style="BI", fname=str(bold_italic_path))

            # Set DejaVu as default font
            pdf.set_font("DejaVu", size=self.font_size)
        else:
            # Set default font
            pdf.set_font(self.font_family, size=self.font_size)

        # Create render context with optional data
        context = RenderContext(pdf, data=data)

        # Render all pages
        for page in self.pages:
            page.render(context)

        # Save PDF
        pdf.output(output_path)

    def __repr__(self) -> str:
        return f"Document(pages={len(self.pages)}, title='{self.title}')"
