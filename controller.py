import datetime
from view.widgets.window import Window7in5

window = Window7in5('resources')

window.calender.set_dates(['%2s' % i for i in range(35)])
window.calender.is_draw_border(True)
window.calender.set_month('January')

window.weather.set_humidity(89.8)
window.weather.set_temp_range(-10.1, 12.2)
window.weather.set_weather(200)
window.weather.set_forecast([(310, -10.1, 11.1)])

window.events.set_events([
    (datetime.datetime.now(), 'asdfasdfasdfasdfasdfsadf'),
    (datetime.datetime.now(),
     'asdfasdfasdfasdfasdfsadfasdfasdfasdfasdfasdfasdfasdfasdf')])

image = window.render()

image.save("text.png")
