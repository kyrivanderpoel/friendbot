import logging


def suppress_loud_loggers():
    loud_info_loggers = ["discord.client", "discord.gateway"]
    for loud_info_logger in loud_info_loggers:
        logging.getLogger(loud_info_logger).setLevel(logging.WARNING)

    loud_debug_loggers = ["discord.http", "asyncio"]
    for loud_debug_logger in loud_debug_loggers:
            logging.getLogger(loud_debug_logger).setLevel(logging.INFO)
