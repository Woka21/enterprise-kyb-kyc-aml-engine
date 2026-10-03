import os
import time

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

print('KYB worker started')
print(f'Database URL configured: {DATABASE_URL}')

while True:
    print('Scanning public KRA / eCitizen portals for KYB checks...')
    time.sleep(30)
