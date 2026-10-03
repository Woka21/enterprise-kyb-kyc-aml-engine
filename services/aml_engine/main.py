import os
import time
import logging
from pathlib import Path

from watchlist_service import load_watchlist, match_against_watchlist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WATCHLIST_PATH = Path(__file__).resolve().parent / "watchlist.csv"

logger.info('AML Engine initialized')
logger.info(f'Watchlist file configured: {WATCHLIST_PATH}')

while True:
    try:
        names = load_watchlist(WATCHLIST_PATH)
        logger.info(f'Loaded {len(names)} AML watchlist entries.')
        sample = ["Alice Wanjiru", "Jane Doe"]
        for name in sample:
            match = match_against_watchlist(name, names)
            logger.info(f'"{name}" => {"MATCH" if match else "CLEAR"}')
        time.sleep(30)
    except Exception as e:
        logger.error(f'Error in AML engine: {e}')
        time.sleep(30)
