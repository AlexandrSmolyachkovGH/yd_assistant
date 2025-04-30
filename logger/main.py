from logger.conf import configure_logging, get_logger_level

logger_level = get_logger_level('MAIN_LOGGER')
main_logger = configure_logging(level=logger_level, console=True, file=False)
