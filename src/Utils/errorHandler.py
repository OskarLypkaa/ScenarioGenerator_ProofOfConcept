import traceback
from utilities.logger import log

class ErrorHandler:
    """Central error handling utility."""

    @staticmethod
    def handle(error: Exception, message: str = ""):
        """Log exception with optional context message."""
        if message:
            log.error(f"{message}: {error}")
        else:
            log.error(f"Exception: {error}")
        log.debug(traceback.format_exc())

# Singleton
errorHandler = ErrorHandler()
