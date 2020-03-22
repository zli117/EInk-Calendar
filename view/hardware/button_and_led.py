import logging
import threading

import RPi.GPIO as GPIO

from controller import Controller

logger = logging.getLogger('EInkUI')


class ButtonAndLed(object):
    def __init__(self,
                 controller: Controller,
                 button_gpio: int = 26,
                 led_gpio: int = 21) -> None:
        self.button_gpio = button_gpio
        self.controller = controller
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led_gpio, GPIO.OUT)
        self.led_gpio = led_gpio

        def call_back(channel: int) -> None:
            def new_thread():
                self.controller.update_and_redraw()
                logger.info('Update of the screen due to button event')

            thread = threading.Thread(target=new_thread)
            thread.start()

        GPIO.add_event_detect(button_gpio,
                              GPIO.FALLING,
                              callback=call_back,
                              bouncetime=500)
        self.led_off()

    def exit(self) -> None:
        self.led_off()
        GPIO.cleanup()

    def led_on(self) -> None:
        GPIO.output(self.led_gpio, GPIO.HIGH)

    def led_off(self) -> None:
        GPIO.output(self.led_gpio, GPIO.LOW)
