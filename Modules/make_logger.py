from logging import DEBUG, Formatter, StreamHandler, getLogger

from rich.logging import RichHandler


def make_logger(name: str):
    logger = getLogger(name)
    logger.setLevel(DEBUG)
    handler = RichHandler(rich_tracebacks=True, markup=True)
    formatter = Formatter("[magenta]%(name)s[/magenta] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
