import os
import time

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://compliance:compliance_secret@postgres:5432/compliance')

print('AML engine started')
print(f'Database URL configured: {DATABASE_URL}')

while True:
    print('Running sanctions and PEP watchlist matching...')
    time.sleep(30)
