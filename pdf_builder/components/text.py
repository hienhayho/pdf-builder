"""Text component - renders text paragraphs with template support."""

import re

from pdf_builder.core import Component, RenderContext
from pdf_builder.exceptions import MissingDataModelError, MissingTemplateFieldError


class Text(Component):
    """
    A text component for rendering paragraphs with template support.

    Supports:
    - Font customization
    - Colors
    - Alignment
    - Multi-line text with wrapping
    - Template placeholders like {{field_name}}
    """

    # Regex pattern to match {{field_name}} placeholders
    PLACEHOLDER_PATTERN = re.compile(r"\{\{(\w+)\}\}")

    def __init__(
        self,
        content: str,
        font_family: str = "Arial",
        font_size: float = 11,
        font_style: str = "",
        color: tuple[int, int, int] = (0, 0, 0),
        align: str = "L",
        line_height: float = 6,
        style: dict | None = None,
    ):
        """
        Initialize a text component.

        Args:
            content: The text content
            font_family: Font family name
            font_size: Font size in points
            font_style: Font style ("B", "I", "U", or combination)
            color: RGB color tuple
            align: Text alignment ("L", "C", "R", "J")
            line_height: Line height in mm
            style: Additional styling
        """
        super().__init__(style)
        self.content = content
        self.font_family = font_family
        self.font_size = font_size
        self.font_style = font_style
        self.color = color
        self.align = align
        self.line_height = line_height

    def get_placeholders(self) -> list[str]:
        """
        Extract all placeholder field names from the content.

        Returns:
            List of field names found in placeholders
        """
        return self.PLACEHOLDER_PATTERN.findall(self.content)

    def get_rendered_content(self, context: RenderContext) -> str:
        """
        Get the content with template placeholders replaced.

        Args:
            context: RenderContext containing the data model

        Returns:
            Content string with placeholders filled from data model
        """
        placeholders = self.get_placeholders()
        rendered_content = self.content

        if placeholders:
            if context.data is None:
                raise MissingDataModelError(placeholders)

            # Replace each placeholder with data from model
            for field_name in placeholders:
                if not hasattr(context.data, field_name):
                    raise MissingTemplateFieldError(
                        field_name, self.__class__.__name__
                    )

                # Get value from data model
                value = getattr(context.data, field_name)

                # Convert to string (handle dates, numbers, etc.)
                if hasattr(value, "strftime"):  # Date/datetime
                    value_str = value.strftime("%d.%m.%Y")
                else:
                    value_str = str(value)

                # Replace placeholder
                rendered_content = rendered_content.replace(
                    f"{{{{{field_name}}}}}", value_str
                )

        return rendered_content

    def render(self, context: RenderContext) -> None:
        """Render the text to the PDF with template placeholders filled."""
        pdf = context.pdf

        # Get rendered content with placeholders replaced
        rendered_content = self.get_rendered_content(context)

        # Get current font family (to preserve Unicode font if set)
        current_font = pdf.font_family or self.font_family

        # Set font
        pdf.set_font(current_font, self.font_style, self.font_size)

        # Set text color
        pdf.set_text_color(*self.color)

        # Render text with multi-line support
        pdf.multi_cell(
            w=0,  # Full width
            h=self.line_height,
            text=rendered_content,
            align=self.align,
        )

        # Reset text color to black
        pdf.set_text_color(0, 0, 0)

    def __repr__(self) -> str:
        preview = self.content[:30] + "..." if len(self.content) > 30 else self.content
        return f"Text('{preview}', font={self.font_family}/{self.font_size})"
