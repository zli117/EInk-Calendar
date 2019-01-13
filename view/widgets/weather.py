from PIL import ImageFont

from view.widgets.panel import PanelWidget
from view.widgets.text import TextWidget
from view.widgets.weather_icon_lookup import WeatherIconLookup


class ForecastWidget(PanelWidget):
    def __init__(self, height: int, width: int, icon_font: ImageFont,
                 text_font: ImageFont, icon_lookup: WeatherIconLookup):
        super().__init__(height, width)

        self.weather_icon = TextWidget(height // 2, width, font=icon_font)
        self.weather_icon.row = 0
        self.weather_icon.col = 0
        self.weather_icon.text = icon_lookup.look_up_with_name('wi-na')
        self.add_child(self.weather_icon)

        self.low_temp_text = TextWidget(height // 4, width, font=text_font)
        self.low_temp_text.row = height // 2
        self.low_temp_text.col = 0
        self.low_temp_text.text = '--'
        self.add_child(self.low_temp_text)

        self.high_temp_text = TextWidget(height // 4, width, font=text_font)
        self.high_temp_text.row = height // 4 * 3
        self.high_temp_text.col = 0
        self.high_temp_text.text = '--'
        self.add_child(self.high_temp_text)

        self.icon_lookup = icon_lookup

    def set_weather(self, id: int):
        unicode = self.icon_lookup.look_up_with_owm_id(id)
        self.weather_icon.text = unicode

    def set_temp_range(self, low: float, high: float):
        self.high_temp_text.text = '%.02f' % high
        self.low_temp_text.text = '%.02f' % low


class WeatherWidget(PanelWidget):
    def __init__(self, height: int, width: int, icon_font: ImageFont,
                 small_icon_font: ImageFont, text_font: ImageFont,
                 icon_lookup: WeatherIconLookup):
        super().__init__(height, width)
        self.icon_lookup = icon_lookup

        self.weather_icon = TextWidget(height // 2, width // 2, font=icon_font)
        self.weather_icon.row = 0
        self.weather_icon.col = 0
        self.weather_icon.text = icon_lookup.look_up_with_name('wi-na')
        self.add_child(self.weather_icon)

        detail_width = width * 0.2
        self.temperature_icon = TextWidget(height // 4, width // 4,
                                           font=small_icon_font)
        self.temperature_icon.row = 0
        self.temperature_icon.col = width // 2
        self.temperature_icon.text = icon_lookup.look_up_with_name(
            'wi-thermometer')
        self.add_child(self.temperature_icon)

        self.temperature_text = TextWidget(height // 4, width // 4,
                                           font=text_font)
        self.temperature_text.row = 0
        self.temperature_text.col = width // 4 * 3
        self.temperature_text.text = '--'
        self.add_child(self.temperature_text)

        self.humidity_icon = TextWidget(height // 4, width // 4,
                                        font=small_icon_font)
        self.humidity_icon.row = height // 4
        self.humidity_icon.col = width // 2
        self.humidity_icon.text = icon_lookup.look_up_with_name('wi-humidity')
        self.add_child(self.humidity_icon)

        self.humidity_text = TextWidget(height // 4, width // 4, font=text_font)
        self.humidity_text.row = height // 4
        self.humidity_text.col = width // 4 * 3
        self.humidity_text.text = '--'
        self.add_child(self.humidity_text)

        self.forecasts = []
        for i in range(4):
            forecast = ForecastWidget(height // 2, width // 4, small_icon_font,
                                      text_font, icon_lookup)
            forecast.row = height // 2
            forecast.col = i * width // 4
            self.add_child(forecast)
            self.forecasts.append(forecast)

    def set_weather(self, id: int):
        unicode = self.icon_lookup.look_up_with_owm_id(id)
        self.weather_icon.text = unicode

    def set_temp_range(self, low: float, high: float):
        self.temperature_text.text = '%.02f\n%.02f' % (low, high)

    def set_humidity(self, humidity: float):
        self.humidity_text.text = '%.02f' % humidity

    def set_forecast(self, forecasts: list):
        for i, forecast in enumerate(forecasts):
            weather, low, high = forecast
            self.forecasts[i].set_weather(weather)
            self.forecasts[i].set_temp_range(low, high)
