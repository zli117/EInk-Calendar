import RPi.GPIO as GPIO

class Button:
    def __init__(self, controller, button_gpio=26):
        self.button_gpio = button_gpio
        self.controller = controller
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def call_back(channel):
            self.controller.update_all()
            self.controller.render_and_display()

        GPIO.add_event_detect(button_gpio, GPIO.FALLING, call_back=call_back,
                              bouncetime=300)

    def exit(self):
        GPIO.cleanup()
