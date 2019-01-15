import RPi.GPIO as GPIO


class ButtonAndLed:
    def __init__(self, controller, button_gpio=26, led_gpio=21):
        self.button_gpio = button_gpio
        self.controller = controller
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led_gpio, GPIO.OUT)
        self.led_gpio = led_gpio

        def call_back(channel):
            self.controller.update_all()
            self.controller.render_and_display()

        GPIO.add_event_detect(button_gpio, GPIO.FALLING, callback=call_back,
                              bouncetime=300)
        self.led_off()

    def exit(self):
        GPIO.cleanup()
        self.led_off()

    def led_on(self):
        GPIO.output(self.led_gpio, GPIO.HIGH)

    def led_off(self):
        GPIO.output(self.led_gpio, GPIO.LOW)
