import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.extra_name = getattr(record, 'extra_name', 'DEFAULT')
        return super().format(record)

def setup_logger(
    name: str, level: int = logging.INFO, file: str = None
) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = CustomFormatter(
        "[%(asctime)s][%(name)s][%(extra_name)s]%(message)s",
    )

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if file:
        fh = logging.FileHandler(file)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

logging.getLogger("pyrogram").setLevel(logging.WARNING)

user_logger = setup_logger("USER", logging.DEBUG)
