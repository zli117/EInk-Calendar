import os

from PIL import Image, ImageDraw, ImageFont

from view.widgets.calendar import CalendarWidget
from view.widgets.event import EventsWidget
from view.widgets.panel import PanelWidget
from view.widgets.weather import WeatherWidget
from view.widgets.weather_icon_lookup import WeatherIconLookup


class Window7in5:
    def __init__(self, resource_dir: str):
        font_large = ImageFont.truetype(os.path.join(
            resource_dir, 'Inconsolata-Regular.ttf'),
                                        size=27)
        font_small = ImageFont.truetype(os.path.join(
            resource_dir, 'Inconsolata-Regular.ttf'),
                                        size=14)
        font_weather_large = ImageFont.truetype(os.path.join(
            resource_dir, 'weathericons-regular-webfont.ttf'),
                                                size=47)
        font_weather_small = ImageFont.truetype(os.path.join(
            resource_dir, 'weathericons-regular-webfont.ttf'),
                                                size=27)

        self.window = PanelWidget(640, 384)

        calendar_size = 28 * 7
        weather_height = 384 - calendar_size

        self._events = EventsWidget(384,
                                    640 - calendar_size,
                                    header_font=font_large,
                                    event_font=font_small)
        self._events.row = 0
        self._events.col = calendar_size
        self.window.add_child(self._events)

        self._calender = CalendarWidget(calendar_size,
                                        calendar_size,
                                        font=font_small)
        self._calender.row = weather_height
        self._calender.col = 0
        self._calender.is_draw_border(True)
        self.window.add_child(self._calender)

        icon_lookup = WeatherIconLookup(
            os.path.join(resource_dir, 'weathericons.xml'))

        self._weather = WeatherWidget(weather_height, calendar_size,
                                      font_weather_large, font_weather_small,
                                      font_small, icon_lookup)
        self._weather.is_draw_border(True)
        self.window.add_child(self._weather)

        self.window.abs_col = 0
        self.window.abs_row = 0

    def render(self):
        image = Image.new('1', (self.window.height, self.window.width), 255)
        draw = ImageDraw.Draw(image)
        self.window.draw(draw)
        return image

    @property
    def events(self):
        return self._events

    @property
    def calender(self):
        return self._calender

    @property
    def weather(self):
        return self._weather

    def show_widget_border(self, show_border: bool):
        self.window.is_draw_border(show_border)
        self.window.is_children_draw_border(show_border)
