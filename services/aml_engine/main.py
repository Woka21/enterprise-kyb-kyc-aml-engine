import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

logger.info('AML Engine initialized')
logger.info(f'Database URL configured: {DATABASE_URL}')

while True:
    try:
        logger.info('Running sanctions and PEP watchlist matching...')
        # TODO: Integrate OpenSanctions database for fuzzy matching
        time.sleep(30)
    except Exception as e:
        logger.error(f'Error in AML engine: {e}')
        time.sleep(30)
