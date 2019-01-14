import datetime

from model.calendar import get_calendar_days, get_month_str
from view.window import Window7in5

window = Window7in5('resources')


class Controller:
    def __init__(self):
        self.window = Window7in5('resources')

    def update_calendar(self):
        self.window.calender.clear_selection()
        self.window.calender.set_month(get_month_str())
        days, selection = get_calendar_days()
        self.window.calender.set_dates(days)
        self.window.calender.set_select_date(selection[0], selection[1], True)

    def update_weather(self):
        self.window.weather.set_humidity(89.8)
        self.window.weather.set_temp_range(-10.1, 12.2)
        self.window.weather.set_weather(200)
        self.window.weather.set_forecast([(310, -10.1, 11.1)])

    def update_events(self):
        self.window.events.set_events([
            (datetime.datetime.now(), 'asdfasdfasdfasdfasdfsadf'),
            (datetime.datetime.now(),
             'asdfasdfasdfasdfasdfsadfasdfasdfasdfasdfasdfasdfasdfasdf')])

    def render(self):
        return self.window.render()


controller = Controller()
controller.update_calendar()
controller.update_weather()
controller.update_events()

image = controller.render()

image.save("text.png")
