"""A wrapper module for logging, debugging, Exceptions management, warnings, etc."""

import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)


# Create a file handler and set the file name
# file_handler = logging.FileHandler('example.log')
# file_handler.setLevel(logging.DEBUG)  # Set the desired logging level for the file handler

# Create a stream handler for console output
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)  # Set the desired logging level for the console handler

# Create a formatter and set it for the handlers
# formatter = logging.Formatter('%(levelname)s: %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)


# logging.basicConfig(level=logging.INFO)

def console(msg: str):
    print(msg)


def debug(msg: str):
    logging.debug(msg=msg)
    console(f"DEBUG: {msg}")


def error(msg: str):
    logging.error(msg=msg)
    console(f"ERROR: {msg}")
    raise Exception(msg)


def warning(msg: str):
    logging.warning(msg=msg)
    console(f"WARNING: {msg}")
    warning(msg=msg)
