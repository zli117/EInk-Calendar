from widgets.panel import PanelWidget
from widgets.text import TextWidget


class CalenderWidget(PanelWidget):
    def __init__(self, height: int, width: int, font=None):
        super().__init__(height, width)
        self.font = font
        children_height = height // 7

        self.month = TextWidget(children_height, width, self.font)
        self.month.row = 0
        self.month.col = 0
        self.add_child(self.month)

        days = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

        cell_width = width // 7
        for i, day in enumerate(days):
            day_text = TextWidget(children_height, cell_width, self.font)
            day_text.row = children_height
            day_text.col = i * cell_width
            day_text.text = day
            self.add_child(day_text)

        self.date_cells = []

        for i in range(5):
            for j in range(7):
                day_text = TextWidget(children_height, cell_width, self.font)
                day_text.row = children_height * (i + 2)
                day_text.col = cell_width * j
                self.add_child(day_text)
                self.date_cells.append(day_text)

    def set_dates(self, dates):
        assert len(dates) == 35
        for i in range(len(dates)):
            self.date_cells[i].text = str(dates[i])

    def set_month(self, month: str):
        self.month.text = month

    def set_select_date(self, row: int, col: int, selected: bool):
        assert 0 <= row < 5 and 0 <= col < 7
        self.date_cells[row * 7 + col].is_draw_border(selected)

    def clear_selection(self):
        for date in self.date_cells:
            date.is_draw_border(False)
