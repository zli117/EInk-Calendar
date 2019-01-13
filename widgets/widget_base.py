from PIL import ImageDraw


class WidgetBase:
    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width
        self._row = 0
        self._col = 0
        self._abs_row = 0
        self._abs_col = 0
        self._children = []
        self._draw_border = False
        self._children_draw_border = False
        self._background = 1
        self._foreground = 0

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row: int):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col: int):
        self._col = col

    @property
    def abs_row(self):
        return self._abs_row

    @abs_row.setter
    def abs_row(self, abs_row):
        self._abs_row = abs_row
        for child in self._children:
            child.abs_row = abs_row + child.row

    @property
    def abs_col(self):
        return self._abs_col

    @abs_col.setter
    def abs_col(self, abs_col):
        self._abs_col = abs_col
        for child in self._children:
            child.abs_col = abs_col + child.col

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = background

    @property
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, foreground):
        self._foreground = foreground

    def is_draw_border(self, draw_border: bool):
        self._draw_border = draw_border

    def is_children_draw_border(self, children_draw_border: bool = False):
        for child in self._children:
            child.is_draw_border(children_draw_border)
            child.is_children_draw_border(children_draw_border)

    def draw(self, draw: ImageDraw):
        if self._draw_border:
            draw.rectangle((self.abs_col, self.abs_row,
                            self.abs_col + self.width - 1,
                            self.abs_row + self.height - 1),
                           outline=self.foreground, fill=self.background)

    def add_child(self, child):
        self._children.append(child)
        child.abs_col = self.abs_col + child.col
        child.abs_row = self.abs_row = child.row
