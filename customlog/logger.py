from enum import Enum, auto
import logging


class Colors(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class CustomFormatter(logging.Formatter):
    
    COLOR_PATTERN = '\033[1;3%dm'
    RESET_COLLOR = '\033[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.INFO: (self.COLOR_PATTERN % Colors.GREEN.value) + self.fmt + self.RESET_COLLOR,
        logging.WARNING: (self.COLOR_PATTERN % Colors.YELLOW.value) + self.fmt + self.RESET_COLLOR,
        logging.ERROR: (self.COLOR_PATTERN % Colors.RED.value) + self.fmt + self.RESET_COLLOR,
        logging.CRITICAL: (self.COLOR_PATTERN % Colors.RED.value) + self.fmt + self.RESET_COLLOR,
        }


    def format(self, record):
        fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt)
        return formatter.format(record)


def create_custom_logger():
    extra = {'app_name':'Super App'}        
    custom_logger = logging.getLogger(__name__)
    custom_handler = logging.StreamHandler()
    custom_logger.setLevel(logging.INFO)
    # custom_handler.setStream(sys.stdout)
    custom_handler.setFormatter(CustomFormatter('%(asctime)s | %(levelname)8s | %(message)s'))
    custom_logger.addHandler(custom_handler)
    custom_logger = logging.LoggerAdapter(custom_logger, extra)
    return custom_logger