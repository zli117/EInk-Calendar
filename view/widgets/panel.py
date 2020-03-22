from PIL import ImageDraw

from view.widgets.widget_base import WidgetBase


class PanelWidget(WidgetBase):
    def __init__(self, height: int, width: int) -> None:
        super().__init__(height, width)

    def draw(self, draw: ImageDraw) -> None:
        super().draw(draw)
        for child in self._children:
            child.draw(draw)
