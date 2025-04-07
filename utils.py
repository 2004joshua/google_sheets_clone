# utils.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='error_log.txt',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
