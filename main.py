import logging

from utils.config_generator import load_or_create_config
from controller import Controller

logging_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('EInkUI')

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    config = load_or_create_config()

    controller = Controller(config, logger)
    controller.run()
