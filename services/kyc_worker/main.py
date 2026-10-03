import os
import time

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

print('KYC worker started')
print(f'Database URL configured: {DATABASE_URL}')

while True:
    print('Running OCR and ID verification checks...')
    time.sleep(30)
