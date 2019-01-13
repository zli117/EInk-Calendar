from PIL import ImageFont, ImageDraw, Image

from widgets.calender import CalenderWidget
from widgets.panel import PanelWidget
from widgets.text import TextWidget

image = Image.new('1', (640, 384), 255)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('fonts/Inconsolata-Regular.ttf', size=27)
font_smaller = ImageFont.truetype('fonts/Inconsolata-Regular.ttf', size=17)

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

window.abs_col = 0
window.abs_row = 0

calender.set_dates(['%2s' % i for i in range(35)])
calender.is_draw_border(True)
calender.set_month('January')

window.draw(draw)

image.save("text.png")
