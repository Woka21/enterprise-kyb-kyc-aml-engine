import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

logger.info('KYB Worker initialized')
logger.info(f'Database URL configured: {DATABASE_URL}')

while True:
    try:
        logger.info('Scanning public KRA / eCitizen portals for KYB checks...')
        # TODO: Integrate Playwright for KRA PIN verification and CR12 checks
        time.sleep(30)
    except Exception as e:
        logger.error(f'Error in KYB worker: {e}')
        time.sleep(30)
