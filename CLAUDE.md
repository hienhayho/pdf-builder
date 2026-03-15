# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PDF Builder is a **container-based PDF generation library** using a component tree architecture similar to modern UI frameworks (React, Flutter, SwiftUI). Documents are built by composing containers and components in a hierarchical structure, built on top of fpdf2.

## Package Management

Use **uv** for all package operations:

```bash
# Install package in development mode
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"

# Run scripts
uv run python examples/cover_page_example.py
```

## Running Examples

Example demonstrates creating a professional cover page with Vietnamese text:

```bash
# Cover page with logo and Vietnamese text
python examples/cover_page_example.py

# Output is saved to examples/output/
```

## Development Commands

```bash
# Format code
black pdf_builder/ examples/

# Lint code
ruff check pdf_builder/

# Run tests (when available)
pytest
```

## Core Architecture

The library follows a **component tree pattern** with three fundamental concepts:

### 1. Component (`pdf_builder/core/component.py`)
Base class for all renderable elements. Every element (text, image, table, container) is a Component.

- **Abstract method**: `render(context: RenderContext) -> None`
- **Style inheritance**: Components inherit styles from parents via `get_style(key, default)`
- **Parent tracking**: Each component knows its parent for style cascade

### 2. Container (`pdf_builder/core/container.py`)
Components that can hold child components. Containers manage:
- Child component lifecycle (parent-child relationships)
- Layout direction (vertical/horizontal)
- Spacing between children
- Background and borders

Key methods:
- `add(*components)` - Add children (chainable)
- `render(context)` - Renders background, then all children with spacing

### 3. RenderContext (`pdf_builder/core/context.py`)
State object passed through the component tree during rendering.

Contains:
- `pdf: FPDF` - The fpdf2 FPDF instance (properly typed for IDE support)
- `data: BaseModel | None` - Optional Pydantic model for dynamic content (see Dynamic Data section below)
- `state: dict[str, Any]` - Shared state dictionary
- Helper methods: `get_current_y()`, `get_page_width()`, etc.

**Type Safety**: The `pdf` attribute is properly typed as `FPDF` from the `fpdf` module, providing full IDE autocomplete and type checking support.

**Dynamic Data**: You can pass a Pydantic model to `Document.render(data=...)` to provide dynamic content that can be accessed across all pages via `context.data`. This is useful for employee names, dates, company info, etc.

### Document Hierarchy

```
Document (pdf_builder/document.py)
└── Page (pdf_builder/containers/page.py)
    ├── Box (container with background/border)
    │   ├── Heading (component)
    │   └── Text (component)
    ├── Section (container with optional title)
    │   └── Table (component)
    ├── Row (horizontal layout container)
    └── Footer (fixed position footer)
```

## Built-in Containers (pdf_builder/containers/)

- **Page** - Represents a PDF page, automatically adds new page to document
- **Box** - Colored box with borders and padding (uses fpdf2 table for rendering)
- **Section** - Logical grouping with optional title and numbering
- **Row** - Horizontal layout container with flex-like `justify` parameter for alignment using `RowJustify` enum (e.g., `RowJustify.SPACE_BETWEEN`)
- **Footer** - Fixed position footer that renders at the bottom of the page using `margin_bottom` parameter

## Built-in Components (pdf_builder/components/)

- **Text** - Paragraphs with wrapping, alignment, and template placeholder support (`{{field_name}}`)
- **Heading** - H1-H6 headings with auto-sizing
- **Image** - Images with alignment and sizing
- **Table** - Auto-layout tables with header styling and row striping
- **Spacer** - Vertical spacing

## Dynamic Data with Pydantic Models and Template Placeholders

The library supports dynamic content using template placeholders (`{{field_name}}`) in Text components. This is ideal for employee-specific data like names, dates, or IDs that change between document instances.

### Best Practices

**DO**: Use template placeholders for dynamic, variable data
- Employee names, IDs
- Report dates
- Department names
- Customer information

**DON'T**: Use template placeholders for static content
- Report titles
- Company branding
- Fixed instructions or quotes
- Standard section headers

### Creating a Data Model

Only include fields that actually vary between document instances:

```python
from datetime import date
from pydantic import BaseModel

class CoverPageData(BaseModel):
    """Data model for cover page - only employee-specific data."""
    employee_name: str
    report_date: date
```

### Using Template Placeholders

```python
from pdf_builder import Document, Page, Text, Row, RowJustify, Footer

# Create data instance with only dynamic fields
data = CoverPageData(
    employee_name="Nguyễn Văn A",
    report_date=date(2026, 3, 27),
)

# Create document
doc = Document(unicode_support=True)
page = Page()

# Static content - hardcoded (NOT templated)
page.add(Text("BÁO CÁO NĂNG LỰC", font_size=20, font_style="B", align="C"))
page.add(Text('"Tự nhận thức chiếm hơn một nửa..."', font_size=11))

# Dynamic content in footer - use template placeholders
footer = Footer(margin_bottom=15)
footer_row = Row(justify=RowJustify.SPACE_BETWEEN)

# Employee name placeholder
left_row = Row()
left_row.add(
    Text("Nhân sự:  ", font_size=10),
    Text("{{employee_name}}", font_size=10, font_style="B")
)
footer_row.add(left_row)

# Date placeholder (auto-formatted as DD.MM.YYYY)
right_row = Row()
right_row.add(
    Text("Date:  ", font_size=10, align="R"),
    Text("{{report_date}}", font_size=10, font_style="B", align="R")
)
footer_row.add(right_row)

footer.add(footer_row)
page.add(footer)
doc.add(page)

# Get required template fields before rendering
required_fields = doc.get_required_fields()
print(f"Required fields: {sorted(required_fields)}")  # ['employee_name', 'report_date']

# Render with data - placeholders automatically filled
doc.render("output.pdf", data=data)
```

### Error Handling

The library automatically validates template fields:

```python
# Missing data model - raises MissingDataModelError
doc.render("output.pdf")  # Error: template fields require a data model

# Missing field in data - raises MissingTemplateFieldError
class IncompleteData(BaseModel):
    employee_name: str  # Missing other required fields

data = IncompleteData(employee_name="John")
doc.render("output.pdf", data=data)  # Error: field 'report_date' not found in data model
```

### Benefits

- **Type Safety**: Pydantic validates data types at runtime
- **Reusability**: Same document template with different data
- **Separation of Concerns**: Data separate from presentation logic
- **Validation**: Automatic detection of missing fields
- **Field Discovery**: `get_required_fields()` shows all template fields
- **Auto-formatting**: Dates automatically formatted as DD.MM.YYYY
- **Across Pages**: Data accessible in all pages

## Enums and Constants

### RowJustify
Enum for Row container justification (similar to CSS flexbox):
- `RowJustify.FLEX_START` - Align to the start (left)
- `RowJustify.FLEX_END` - Align to the end (right)
- `RowJustify.CENTER` - Center items
- `RowJustify.SPACE_BETWEEN` - Space between items (commonly used for footers)
- `RowJustify.SPACE_AROUND` - Space around items

Example:
```python
from pdf_builder import Row, RowJustify, Text

footer_row = Row(justify=RowJustify.SPACE_BETWEEN)
footer_row.add(Text("Left content"), Text("Right content"))
```

## Type Hints Convention

Follow modern Python type hint practices:
- Use `dict` instead of `Dict`
- Use `list` instead of `List`
- Use `tuple` instead of `Tuple`
- Use `| None` instead of `Optional[T]`
- Example: `def add(self, children: list[Component] | None = None) -> Container:`

## Creating New Components

### Leaf Component (extends Component):

```python
from pdf_builder.core import Component, RenderContext

class CustomComponent(Component):
    def __init__(self, data, style: dict | None = None):
        super().__init__(style)
        self.data = data

    def render(self, context: RenderContext) -> None:
        # Use context.pdf (fpdf2 instance) to render
        context.pdf.cell(text=self.data)
```

### Container Component (extends Container):

```python
from pdf_builder.core import Container, RenderContext

class CustomContainer(Container):
    def render(self, context: RenderContext) -> None:
        # Render background/borders if needed
        self._render_background(context)

        # Render all children
        super().render(context)
```

## Important Implementation Details

### Box Rendering
Box containers use fpdf2's table context manager to render backgrounds and borders. Children are rendered inside a table cell for proper styling.

### Style Inheritance
Styles cascade from parent to child. When getting a style property, if not found in the component's style dict, it falls back to parent's style recursively.

### Parent-Child Relationships
When adding children via `add()`, the container automatically calls `child.set_parent(self)` to establish the parent-child relationship for style inheritance.

## Project Structure

```
pdf_builder/
├── __init__.py          # Public API exports
├── document.py          # Document class (entry point)
├── core/                # Core abstractions
│   ├── component.py     # Base Component class
│   ├── container.py     # Base Container class
│   └── context.py       # RenderContext
├── containers/          # Built-in containers
│   ├── page.py
│   ├── box.py
│   ├── footer.py
│   ├── section.py
│   └── row.py
└── components/          # Built-in components
    ├── text.py
    ├── heading.py
    ├── image.py
    ├── table.py
    └── spacer.py
```

## Adding New Components to the Library

1. Create new file in `pdf_builder/components/` or `pdf_builder/containers/`
2. Extend `Component` or `Container` base class
3. Implement the `render(context: RenderContext)` method
4. Export in the appropriate `__init__.py` file
5. Update `pdf_builder/__init__.py` to include in public API
- use uv to add install packages and python script, not use pure python
- Always use Context7 when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.
- remove logs when debuging done
- ALWAYS use uv run