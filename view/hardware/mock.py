from PIL import Image

from utils.config_generator import Configurations
from controller import Controller


class ButtonAndLed(object):
    def __init__(self, controller: Controller):
        pass

    def exit(self) -> None:
        print('EXIT')

    def led_on(self) -> None:
        print('LED ON')

    def led_off(self) -> None:
        print('LED OFF')


class EPD:
    def __init__(self, config: Configurations) -> None:
        self.save_path = config.debug_save_path

    # Hardware reset
    def reset(self) -> None:
        pass

    def send_command(self, command: str) -> None:
        pass

    def send_data(self, data: str) -> None:
        pass

    def wait_until_idle(self) -> None:
        pass

    def init(self):
        pass

    def get_buffer(self, image: Image) -> Image:
        return image

    def display(self, image: Image) -> None:
        print(self.save_path)
        image.save(self.save_path)

    def clear(self, color: int) -> None:
        pass

    def sleep(self) -> None:
        pass
