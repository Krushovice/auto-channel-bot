import logging
import os
from logging.handlers import RotatingFileHandler


# Корень проекта: app/.. -> корень
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.getenv("LOG_DIR", os.path.join(PROJECT_ROOT, "logs"))
LOG_PATH = os.path.join(LOG_DIR, "app.log")


FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    # Базовая конфигурация для консоли
    logging.basicConfig(level=logging.INFO, format=FMT, datefmt=DATEFMT)

    # Файловый хендлер только для ошибок и выше
    file_handler = RotatingFileHandler(
        LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(FMT, datefmt=DATEFMT))

    root = logging.getLogger()
    root.addHandler(file_handler)
