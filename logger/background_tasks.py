from logger.conf import configure_logging, get_logger_level

logger_level = get_logger_level('BACKGROUND_LOGGER')
background_logger = configure_logging(level=logger_level, console=True, file=False)
