from pathlib import Path
from loguru import logger


BASE_DIR = Path(__file__).resolve().parent.parent

PATH_TO_LOGS = BASE_DIR / "jun-jobs-bot" / "logs" / "logs.log"

LOGGER_FORMAT = "{time:YYYY.MM.DD - HH:mm:ss} - {level} - {message} "

LOGGER = logger.add(
    sink=PATH_TO_LOGS,
    level="INFO",
    format=LOGGER_FORMAT,
)
