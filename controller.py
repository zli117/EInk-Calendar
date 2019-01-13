from PIL import ImageFont, ImageDraw, Image

from widgets.calender import CalenderWidget
from widgets.panel import PanelWidget
from widgets.text import TextWidget
from widgets.weather import WeatherWidget
from widgets.weather_icon_lookup import WeatherIconLookup

image = Image.new('1', (640, 384), 255)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('fonts/Inconsolata-Regular.ttf', size=27)
font_smaller = ImageFont.truetype('fonts/Inconsolata-Regular.ttf', size=14)
font_weather_text = ImageFont.truetype('fonts/Inconsolata-Regular.ttf', size=14)
font_weather_big = ImageFont.truetype(
    'fonts/weathericons-regular-webfont.ttf', size=47)
font_weather_small = ImageFont.truetype(
    'fonts/weathericons-regular-webfont.ttf', size=27)

window = PanelWidget(640, 384)

text1 = TextWidget(40, 640 - 192, font=font)
text1.row = 0
text1.col = 192
text1.text = 'Events'
text1.is_draw_border(True)
text1.background = 0
text1.foreground = 1
window.add_child(text1)

calender = CalenderWidget(192, 192, font=font_smaller)
calender.row = 192
calender.col = 0
window.add_child(calender)

calender.set_dates(['%2s' % i for i in range(35)])
calender.is_draw_border(True)
calender.set_month('January')

icon_lookup = WeatherIconLookup('fonts/weathericons.xml')
weather = WeatherWidget(192, 192, font_weather_big, font_weather_small,
                        font_weather_text, icon_lookup)
weather.is_draw_border(True)
weather.set_humidity(89.8)
weather.set_temp_range(-10.1, 12.2)
weather.set_weather(200)
weather.set_forecast([(310, -10.1, 11.1)])
window.add_child(weather)


window.abs_col = 0
window.abs_row = 0

window.draw(draw)

image.save("text.png")
