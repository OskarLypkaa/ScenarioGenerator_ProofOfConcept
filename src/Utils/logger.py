import os

from loguru import logger
from utilities.settings import settings


os.makedirs(settings.LOGS_OUTPUT_DIR, exist_ok=True)
logFilePath = os.path.join(settings.LOGS_OUTPUT_DIR, "app.log")

# Remove the default logger configuration
logger.remove()

logger.add(
    logFilePath,
    rotation="5 MB",  # Rotate the file after it reaches 5 MB
    retention="10 days",  # Keep old log files for 10 days
    compression="zip",  # Compress old log files into ZIP archives
    level="DEBUG",  # Log level (capture everything from DEBUG and above)
    backtrace=True,  # Extended stack trace on exceptions
    diagnose=True,  # Include variable values in exceptions
)


logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green> | <level>{level}</level> | <cyan>{module}</cyan> - <level>{message}</level>",
)

# Singleton
log = logger
