# utils.py

import logging

def setup_logging():
    """
    Set up logging configuration to log errors to error_log.txt.
    """
    logging.basicConfig(
        filename='error_log.txt',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
