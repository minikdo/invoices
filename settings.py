import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INVOICE_DIR = os.path.join(BASE_DIR, 'invoices')

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

BUNDLE_DIR = os.path.join(BASE_DIR, 'bundles')

with open('sendername.txt', 'r') as file:
    SENDER = file.read().strip()

with open('ibans.json', 'r') as file:
    SENDER_IBAN_MAP = json.load(file)

SENDER_IBAN = SENDER_IBAN_MAP.keys()
