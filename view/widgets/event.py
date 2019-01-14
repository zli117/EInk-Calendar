import datetime

from PIL import ImageFont, ImageDraw

from view.widgets.panel import PanelWidget
from view.widgets.text import TextWidget


class EventWidget(PanelWidget):
    def __init__(self, height: int, width: int, event_font: ImageFont):
        super().__init__(height, width)
        self.date = datetime.datetime.now()
        self.font = event_font
        self.event = ''
        self._show = False

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, show: bool):
        self._show = show

    def set_date(self, date: datetime.datetime):
        self.date = date

    def set_event(self, event: str):
        self.event = event

    def draw(self, draw: ImageDraw):
        if not self.show:
            return
        horizontal_pad = self.width // 25
        bottom_pad = self.height // 4
        draw.line((self.abs_col + horizontal_pad,
                   self.abs_row + self.height - bottom_pad,
                   self.abs_col + self.width - horizontal_pad,
                   self.abs_row + self.height - bottom_pad),
                  fill=self.foreground)
        text_w, text_h = self.font.getsize(' ')
        polygon_pts = ((self.abs_col + horizontal_pad,
                        self.abs_row + self.height - bottom_pad),
                       (self.abs_col + horizontal_pad,
                        self.abs_row + self.height - bottom_pad - text_h),
                       (self.abs_col + horizontal_pad + text_w * 8,
                        self.abs_row + self.height - bottom_pad - text_h),
                       (self.abs_col + horizontal_pad + text_w * 9,
                        self.abs_row + self.height - bottom_pad))
        date_str = datetime.datetime.strftime(self.date, ' %b %d')
        draw.polygon(polygon_pts, fill=self.foreground)
        draw.text((self.abs_col + horizontal_pad,
                   self.abs_row + self.height - bottom_pad - text_h), date_str,
                  fill=self.background, font=self.font)
        event_max_chars = (self.width - 2 * horizontal_pad) * 4 // 5 // text_w
        if len(self.event) > event_max_chars:
            self.event = self.event[:event_max_chars - 3] + '...'
        draw.text((self.abs_col + (self.width - 2 * horizontal_pad) // 5
                   + horizontal_pad,
                   self.abs_row + self.height - bottom_pad - text_h),
                  self.event, fill=self.foreground, font=self.font)


class EventsWidget(PanelWidget):
    def __init__(self, height: int, width: int, header_font: ImageFont,
                 event_font: ImageFont):
        super().__init__(height, width)
        header = TextWidget(height // 10, width, font=header_font)
        header.row = 0
        header.col = 0
        header.text = 'Events'
        header.foreground = self.background
        header.background = self.foreground
        header.is_draw_border(True)
        self.add_child(header)

        event_top = height // 5
        self.event_widgets = []
        while event_top < self.width:
            event = EventWidget(height // 10, width, event_font=event_font)
            event.row = event_top
            event.col = 0
            self.event_widgets.append(event)
            self.add_child(event)
            event_top += height // 10

    def set_events(self, events: list):
        for event_widget in self.event_widgets:
            event_widget.show = False
        counter = 0
        for date, text in events:
            event_widget = self.event_widgets[counter]
            event_widget.show = True
            event_widget.set_date(date)
            event_widget.set_event(text)
            counter += 1
            if counter > len(self.event_widgets):
                break
