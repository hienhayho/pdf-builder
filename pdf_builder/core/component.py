"""Base Component class - the foundation of all renderable elements."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import RenderContext


class Component(ABC):
    """
    Abstract base class for all renderable components.

    Every element in the PDF (text, image, table, container) is a Component.
    Components know how to render themselves and can be styled.
    """

    def __init__(self, style: dict | None = None):
        """
        Initialize a component.

        Args:
            style: Optional styling dictionary (padding, margin, colors, etc.)
        """
        self.style = style or {}
        self.parent: "Component | None" = None

    @abstractmethod
    def render(self, context: "RenderContext") -> None:
        """
        Render this component to the PDF.

        Args:
            context: The rendering context containing the PDF instance and state
        """
        pass

    def get_style(self, key: str, default=None):
        """
        Get a style value, with fallback to parent's style.

        Args:
            key: Style property name
            default: Default value if not found

        Returns:
            Style value or default
        """
        if key in self.style:
            return self.style[key]
        if self.parent:
            return self.parent.get_style(key, default)
        return default

    def set_parent(self, parent: "Component") -> None:
        """Set the parent component for style inheritance."""
        self.parent = parent

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(style={self.style})"
