from typing import List

from PIL import ImageDraw


class WidgetBase(object):
    def __init__(self, height: int, width: int) -> None:
        self._height = height
        self._width = width
        self._row = 0
        self._col = 0
        self._abs_row = 0
        self._abs_col = 0
        self._children: List[WidgetBase] = []
        self._draw_border = False
        self._children_draw_border = False
        self._background = 255
        self._foreground = 0

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, row: int) -> None:
        self._row = row

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, col: int) -> None:
        self._col = col

    @property
    def abs_row(self) -> int:
        return self._abs_row

    @abs_row.setter
    def abs_row(self, abs_row: int) -> None:
        self._abs_row = abs_row
        for child in self._children:
            child.abs_row = abs_row + child.row

    @property
    def abs_col(self) -> int:
        return self._abs_col

    @abs_col.setter
    def abs_col(self, abs_col: int) -> None:
        self._abs_col = abs_col
        for child in self._children:
            child.abs_col = abs_col + child.col

    @property
    def background(self) -> int:
        return self._background

    @background.setter
    def background(self, background: int) -> None:
        self._background = background

    @property
    def foreground(self) -> int:
        return self._foreground

    @foreground.setter
    def foreground(self, foreground: int) -> None:
        self._foreground = foreground

    def is_draw_border(self, draw_border: bool) -> None:
        self._draw_border = draw_border

    def is_children_draw_border(self,
                                children_draw_border: bool = False) -> None:
        for child in self._children:
            child.is_draw_border(children_draw_border)
            child.is_children_draw_border(children_draw_border)

    def draw(self, draw: ImageDraw) -> None:
        if self._draw_border:
            draw.rectangle(
                (self.abs_col, self.abs_row, self.abs_col + self.width - 1,
                 self.abs_row + self.height - 1),
                outline=self.foreground,
                fill=self.background)

    def add_child(self, child: WidgetBase) -> None:
        self._children.append(child)
        child.abs_col = self.abs_col + child.col
        child.abs_row = self.abs_row + child.row
