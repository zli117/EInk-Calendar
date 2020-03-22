from PIL import ImageDraw, ImageFont

from view.widgets.alignments import Alignments
from view.widgets.widget_base import WidgetBase


class TextWidget(WidgetBase):
    def __init__(self, height: int, width: int, font: ImageFont = None):
        super().__init__(height, width)
        self._text = ''
        self._font = font
        self._vertical_align = Alignments.CENTER
        self._horizontal_align = Alignments.CENTER

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def vertical_alignment(self):
        return self._vertical_align

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment):
        self._vertical_align = vertical_alignment

    @property
    def horizontal_alignment(self):
        return self._horizontal_align

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment):
        self._horizontal_align = horizontal_alignment

    def draw(self, draw: ImageDraw):
        super().draw(draw)
        font_w, font_h = draw.textsize(self._text, font=self._font)
        if font_h <= self.height and font_w <= self.width:
            horizontal_offset = self.abs_col
            if self._horizontal_align == Alignments.CENTER:
                horizontal_offset += (self.width - font_w) // 2
            elif self._horizontal_align == Alignments.RIGHT:
                horizontal_offset += self.width - font_w
            vertical_offset = self.abs_row
            if self._vertical_align == Alignments.CENTER:
                vertical_offset += (self.height - font_h) // 2 - 1
            elif self._vertical_align == Alignments.BOTTOM:
                vertical_offset += self.height - font_h
            draw.text((horizontal_offset, vertical_offset),
                      self.text,
                      fill=self.foreground,
                      font=self._font)
