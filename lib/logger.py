import logging
import sys
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def setup_logger(name: str, log_file: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter with time, level, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console output
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    # Rotating file logs (prevents huge files)
    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger

def get_logger(name):
    return logging.getLogger(name)
# Example usage
'''
logger = setup_logger("my_app", "app.log")
logger.info("Logger started")
logger.warning("Something might be off…")
logger.error("Something went wrong!")
'''