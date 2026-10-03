import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

logger.info('KYC Worker initialized')
logger.info(f'Database URL configured: {DATABASE_URL}')

while True:
    try:
        logger.info('Running OCR and ID verification checks...')
        # TODO: Integrate Tesseract OCR and OpenCV for ID document processing
        time.sleep(30)
    except Exception as e:
        logger.error(f'Error in KYC worker: {e}')
        time.sleep(30)
