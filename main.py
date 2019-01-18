import logging
import time

from model.calendar import get_calendar_days, get_month_str
from model.events import GoogleCalendarEvents
from model.weather import OpenWeatherMapModel
from utils.config_generator import Configurations, load_or_create_config
from view.hardware import epd7in5
from view.hardware.button_led import ButtonAndLed
from view.window import Window7in5

logging_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('EInkUI')

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


class Controller:
    def __init__(self, config: Configurations):
        self.window = Window7in5('resources')
        self.events = GoogleCalendarEvents(config.google_credential)
        for calendar_id in config.selected_calendars:
            self.events.select_calendar(calendar_id)
        self.weather = OpenWeatherMapModel(config.owm_token, config.city_id)
        self.weather.temperature_unit = config.units
        self.epd = epd7in5.EPD()
        self.epd.init()
        self.button_and_led = ButtonAndLed(self)
        self.updating_flag = False

    def update_calendar(self):
        self.window.calender.clear_selection()
        self.window.calender.set_month(get_month_str())
        days, selection = get_calendar_days()
        self.window.calender.set_dates(days)
        self.window.calender.set_select_date(selection[0], selection[1], True)

    def update_weather(self):
        weather_id, low, high, humidity = self.weather.get_current_weather()
        self.window.weather.set_weather(weather_id)
        self.window.weather.set_temp_range(low, high)
        self.window.weather.set_humidity(humidity)
        forecasts = self.weather.get_daily_forecast()
        forecasts = list(map(lambda forecast: forecast[:-1], forecasts))
        self.window.weather.set_forecast(forecasts)

    def update_events(self):
        events = self.events.get_sorted_events()
        self.window.events.set_events(events)

    def _update_all(self):
        self.update_events()
        self.update_weather()
        self.update_calendar()

    def _render_and_display(self):
        image = self.window.render()
        self.epd.display(self.epd.get_buffer(image))

    def update_and_redraw(self):
        if self.updating_flag:
            return
        self.updating_flag = True
        self.button_and_led.led_on()
        self._update_all()
        self._render_and_display()
        self.button_and_led.led_off()
        self.updating_flag = False

    def run(self):
        try:
            while True:
                self.update_and_redraw()
                logger.info('Periodic update of the screen')
                time.sleep(3600)

        except KeyboardInterrupt:
            logger.info('Clearing screen on exit')
            self.epd.clear(0xFE)
            self.epd.sleep()
            self.button_and_led.exit()


config = load_or_create_config()

controller = Controller(config)
controller.run()
