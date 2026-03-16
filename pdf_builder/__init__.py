"""
PDF Builder - A container-based PDF generation library.

This library provides a clean, component-based architecture for creating
PDF documents with precise layout control.

Example:
    >>> from pdf_builder import Document, Page, Box, Heading, Text
    >>>
    >>> doc = Document()
    >>> page = Page()
    >>>
    >>> box = Box(background_color=(255, 102, 0), padding=10)
    >>> box.add(Heading("My Title", level=1))
    >>> box.add(Text("Some content here"))
    >>>
    >>> page.add(box)
    >>> doc.add(page)
    >>>
    >>> doc.render("output.pdf")
"""

__version__ = "0.1.0"

# Core classes
from .core import Component, Container, RenderContext

# Containers
from .containers import Box, Footer, Page, Row, RowJustify, Section

# Components
from .components import Heading, Image, Line, Spacer, Table, Text, TocItem

# Exceptions
from .exceptions import (
    MissingDataModelError,
    MissingTemplateFieldError,
    PDFBuilderException,
)

# Main document class
from .document import Document

__all__ = [
    # Core
    "Component",
    "Container",
    "RenderContext",
    # Containers
    "Box",
    "Footer",
    "Page",
    "Row",
    "RowJustify",
    "Section",
    # Components
    "Heading",
    "Image",
    "Line",
    "Spacer",
    "Table",
    "Text",
    "TocItem",
    # Exceptions
    "MissingDataModelError",
    "MissingTemplateFieldError",
    "PDFBuilderException",
    # Document
    "Document",
]
