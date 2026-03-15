"""Image component - renders images."""

from pdf_builder.core import Component, RenderContext


class Image(Component):
    """
    An image component for rendering images.

    Supports:
    - Auto-sizing
    - Manual width/height
    - Alignment
    - Aspect ratio preservation
    """

    def __init__(
        self,
        path: str,
        width: float | None = None,
        height: float | None = None,
        align: str = "L",
        keep_aspect_ratio: bool = True,
        style: dict | None = None,
    ):
        """
        Initialize an image component.

        Args:
            path: Path to the image file
            width: Image width in mm (None = auto)
            height: Image height in mm (None = auto)
            align: Image alignment ("L", "C", "R")
            keep_aspect_ratio: Preserve aspect ratio
            style: Additional styling
        """
        super().__init__(style)
        self.path = path
        self.width = width
        self.height = height
        self.align = align
        self.keep_aspect_ratio = keep_aspect_ratio

    def render(self, context: RenderContext) -> None:
        """Render the image."""
        pdf = context.pdf

        # Get image info to calculate dimensions if needed
        from PIL import Image as PILImage

        img = PILImage.open(self.path)
        img_width_px, img_height_px = img.size

        # Calculate dimensions in mm (assuming 96 DPI)
        px_to_mm = 25.4 / 96

        if self.width and not self.height and self.keep_aspect_ratio:
            # Calculate height based on width
            aspect_ratio = img_height_px / img_width_px
            calculated_height = self.width * aspect_ratio
        elif self.height and not self.width and self.keep_aspect_ratio:
            # Calculate width based on height
            aspect_ratio = img_width_px / img_height_px
            calculated_width = self.height * aspect_ratio
            self.width = calculated_width
            calculated_height = self.height
        elif not self.width and not self.height:
            # Use original dimensions
            self.width = img_width_px * px_to_mm
            calculated_height = img_height_px * px_to_mm
        else:
            calculated_height = self.height

        # Calculate position based on alignment
        x = None
        if self.align == "C":
            if self.width:
                x = (context.get_page_width() - self.width) / 2 + pdf.l_margin
        elif self.align == "R":
            if self.width:
                x = context.get_page_width() - self.width + pdf.l_margin

        # Render image
        pdf.image(
            self.path,
            x=x,
            w=self.width,
            h=calculated_height,
            keep_aspect_ratio=self.keep_aspect_ratio,
        )

        # Move to next line
        pdf.ln(5)

    def __repr__(self) -> str:
        return f"Image(path='{self.path}', {self.width}x{self.height})"
