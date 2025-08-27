import logging
import os
import sys
import tempfile
from logging.handlers import RotatingFileHandler

from core.config import settings

FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
MAX_BYTES = 10 * 1024 * 1024
BACKUPS = 10


def _lvl(name: str, default=logging.INFO) -> int:
    return getattr(logging, str(name).upper(), default)


def _resolve_log_dir(
    preferred: str,
    app_name: str,
) -> tuple[str | None, list[str]]:
    """
    Пытается создать и проверить права на запись в каталоги по очереди:
      1) preferred
      2) ./logs
      3) /tmp/<app_name>-logs
    Возвращает (выбранный_каталог_или_None, список_что_пробовали).
    """
    tried: list[str] = []
    candidates = [
        preferred,
        os.path.abspath("./logs"),
        os.path.join(tempfile.gettempdir(), f"{app_name}-logs"),
    ]

    for d in candidates:
        tried.append(d)
        try:
            os.makedirs(d, exist_ok=True)
            test_path = os.path.join(d, ".write_test")
            with open(test_path, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(test_path)
            return d, tried
        except Exception:
            continue

    return None, tried


def setup_logging() -> None:
    """Консоль + 2 файла (INFO/ERROR) с фоллбэком директории. Повторные вызовы — no-op."""
    if getattr(setup_logging, "_configured", False):
        return

    cfg = settings.logger  # LoggingConfig из твоих nested settings

    root = logging.getLogger()
    root.setLevel(_lvl(cfg.log_level))

    # убрать дефолтные хендлеры
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter(FMT, datefmt=DATEFMT)

    # --- консоль (journalctl) ---
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(_lvl(cfg.console_level))
    console.setFormatter(fmt)
    root.addHandler(console)

    # --- подобрать рабочую директорию логов ---
    log_dir, tried = _resolve_log_dir(cfg.log_dir, cfg.app_name)
    if not log_dir:
        root.warning(
            "Нет прав на запись ни в один каталог логов: %s — работаем только с консолью.",
            ", ".join(tried),
        )
        setup_logging._configured = True
        return

    info_log_path = os.path.join(log_dir, f"{cfg.app_name}.info.log")
    err_log_path = os.path.join(log_dir, f"{cfg.app_name}.error.log")

    # --- файл INFO+ ---
    try:
        info_file = RotatingFileHandler(
            info_log_path,
            maxBytes=MAX_BYTES,
            backupCount=BACKUPS,
            encoding="utf-8",
        )
        info_file.setLevel(_lvl(cfg.file_level))
        info_file.setFormatter(fmt)
        root.addHandler(info_file)
    except Exception as e:
        root.warning(
            "Не удалось подключить info-файл логов (%s): %s",
            info_log_path,
            e,
        )

    # --- файл ERROR+ ---
    try:
        err_file = RotatingFileHandler(
            err_log_path,
            maxBytes=MAX_BYTES,
            backupCount=BACKUPS,
            encoding="utf-8",
        )
        err_file.setLevel(logging.ERROR)
        err_file.setFormatter(fmt)
        root.addHandler(err_file)
    except Exception as e:
        root.warning(
            "Не удалось подключить error-файл логов (%s): %s",
            err_log_path,
            e,
        )

    # Понизим/поднимем болтливость библиотек
    logging.getLogger("aiogram").setLevel(_lvl(cfg.aiogram_level))
    logging.getLogger("aiosmtplib").setLevel(_lvl(cfg.smtp_level))

    setup_logging._configured = True
    root.info(
        "Logging initialized | chosen_dir=%s | preferred=%s | app=%s | level=%s",
        log_dir,
        cfg.log_dir,
        cfg.app_name,
        cfg.log_level,
    )
