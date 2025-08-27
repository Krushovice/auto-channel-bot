import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Корень проекта: app/.. -> корень
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

# ENV с умолчаниями
APP_NAME = os.getenv("APP_NAME", "jp_cars_bot")
LOG_DIR = os.getenv("LOG_DIR", os.path.join(PROJECT_ROOT, "logs"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # корневой уровень
CONSOLE_LEVEL = os.getenv("CONSOLE_LEVEL", "INFO").upper()  # уровень консоли
FILE_LEVEL = os.getenv("FILE_LEVEL", "INFO").upper()  # уровень файла app.info.log
AIOGRAM_LEVEL = os.getenv("AIOGRAM_LEVEL", "INFO").upper()
SMTP_LEVEL = os.getenv("SMTP_LEVEL", "INFO").upper()

INFO_LOG = os.path.join(LOG_DIR, "app.info.log")
ERR_LOG = os.path.join(LOG_DIR, "app.error.log")


def setup_logging() -> None:
    """Единоразовая настройка логов (консоль + два файла)."""
    if getattr(setup_logging, "_configured", False):
        return

    os.makedirs(LOG_DIR, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)

    # Сброс возможных дефолтных хендлеров (важно при повторном импорте/тестах)
    for h in list(root.handlers):
        root.removeHandler(h)

    formatter = logging.Formatter(FMT, datefmt=DATEFMT)

    # --- Консоль (для systemd/journalctl) ---
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(CONSOLE_LEVEL)
    console.setFormatter(formatter)
    root.addHandler(console)

    # --- Файл INFO+ ---
    info_file = RotatingFileHandler(
        INFO_LOG,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    info_file.setLevel(FILE_LEVEL)
    info_file.setFormatter(formatter)
    root.addHandler(info_file)

    # --- Файл ERROR+ ---
    err_file = RotatingFileHandler(
        ERR_LOG,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    err_file.setLevel(logging.ERROR)
    err_file.setFormatter(formatter)
    root.addHandler(err_file)

    # Шум гасим/подкручиваем
    logging.getLogger("aiogram").setLevel(AIOGRAM_LEVEL)
    logging.getLogger("aiosmtplib").setLevel(SMTP_LEVEL)

    # Логируем необработанные исключения (чтобы видеть stacktrace в файле)
    def _excepthook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            root.info("Interrupted by user")
            return
        root.exception(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_tb),
        )

    sys.excepthook = _excepthook

    setup_logging._configured = True
    root.info(
        "Logging initialized | dir=%s | level=%s",
        os.path.abspath(LOG_DIR),
        LOG_LEVEL,
    )
