"""Custom exceptions for pdf-builder."""


class PDFBuilderException(Exception):
    """Base exception for pdf-builder."""

    pass


class MissingTemplateFieldError(PDFBuilderException):
    """Raised when a template field is missing from the data model."""

    def __init__(self, field_name: str, component_type: str):
        """
        Initialize the exception.

        Args:
            field_name: The name of the missing field
            component_type: The type of component that has the missing field
        """
        self.field_name = field_name
        self.component_type = component_type
        super().__init__(
            f"Template field '{field_name}' not found in data model "
            f"(used in {component_type})"
        )


class MissingDataModelError(PDFBuilderException):
    """Raised when template fields are used but no data model is provided."""

    def __init__(self, fields: list[str]):
        """
        Initialize the exception.

        Args:
            fields: List of template fields that require a data model
        """
        self.fields = fields
        super().__init__(
            f"Template fields {fields} require a data model, "
            f"but none was provided to Document.render()"
        )
