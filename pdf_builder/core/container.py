"""Container class - components that can hold other components."""

from typing import TYPE_CHECKING

from .component import Component

if TYPE_CHECKING:
    from .context import RenderContext


class Container(Component):
    """
    Abstract container that can hold child components.

    Containers manage:
    - Child component lifecycle
    - Layout direction (vertical/horizontal)
    - Spacing between children
    - Background and borders
    """

    def __init__(
        self,
        children: list[Component] | None = None,
        layout: str = "vertical",
        spacing: float = 0,
        style: dict | None = None,
    ):
        """
        Initialize a container.

        Args:
            children: Initial child components
            layout: Layout direction - "vertical" or "horizontal"
            spacing: Space between children (in mm or pt)
            style: Styling dictionary
        """
        super().__init__(style)
        self.children: list[Component] = children or []
        self.layout = layout
        self.spacing = spacing

        # Set parent for all children
        for child in self.children:
            child.set_parent(self)

    def add(self, *components: Component) -> "Container":
        """
        Add one or more child components.

        Args:
            *components: Components to add

        Returns:
            Self for method chaining
        """
        for component in components:
            component.set_parent(self)
            self.children.append(component)
        return self

    def render(self, context: "RenderContext") -> None:
        """
        Render this container and all its children.

        Default implementation:
        1. Render container background/border
        2. Render each child
        3. Add spacing between children
        """
        # Render background if specified
        self._render_background(context)

        # Render children
        for i, child in enumerate(self.children):
            child.render(context)

            # Add spacing between children (except after last)
            if i < len(self.children) - 1 and self.spacing > 0:
                if self.layout == "vertical":
                    context.pdf.ln(self.spacing)

    def _render_background(self, context: "RenderContext") -> None:
        """Render container background and borders (to be overridden)."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(children={len(self.children)}, layout={self.layout})"
