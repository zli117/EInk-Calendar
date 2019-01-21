from PIL import Image

from utils.config_generator import Configurations


class ButtonAndLed:
    def __init__(self, controller):
        pass

    def exit(self):
        print('EXIT')

    def led_on(self):
        print('LED ON')

    def led_off(self):
        print('LED OFF')


class EPD:
    def __init__(self, config: Configurations):
        self.save_path = config.debug_save_path

    # Hardware reset
    def reset(self):
        pass

    def send_command(self, command):
        pass

    def send_data(self, data):
        pass

    def wait_until_idle(self):
        pass

    def init(self):
        pass

    def get_buffer(self, image: Image):
        return image

    def display(self, image: Image):
        print(self.save_path)
        image.save(self.save_path)

    def clear(self, color):
        pass

    def sleep(self):
        pass
