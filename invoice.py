#!/usr/bin/env python3

import os

from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from tabulate import tabulate
from types import SimpleNamespace
from datetime import timedelta

from splitamount import SplitAmount


OFFICE = "40105010961000009071970892"
SHOP = "94105010961000000101093797"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INVOICE_DIR = os.path.join(BASE_DIR, 'invoices')

templates = read_templates(os.path.join(BASE_DIR, 'templates'))

invoices = []

for file in os.listdir(INVOICE_DIR):
    _, ext = os.path.splitext(file)
    if 'pdf' in ext:
        result = extract_data(os.path.join(INVOICE_DIR, file),
                              templates=templates)
        try:
            result['days_due']
        except Exception:
            pass
        else:
            result['date_due'] = result['date'] + timedelta(
                days=int(result['days_due']))

        invoices.append(result)


headers = {}
for x in invoices[0].keys():
    headers[x] = x

print(tabulate(invoices, headers=headers))


def get_sender_iban(account) -> str:
    """ Orange invoices per shop or office """
    if account == "71103019317040000050821433" or\
       account == "20103019317040000051568184" or\
       account == "40103019317040000052317828":
        return SHOP
    return OFFICE


for invoice in invoices:
    d = SimpleNamespace(**invoice)

    invoice['date'] = d.date.strftime('%Y%m%d')
    invoice['date_due'] = d.date_due.strftime('%Y%m%d')
    invoice['amount'] = SplitAmount(d.amount).get_full_amount()
    invoice['nrb'] = d.iban[2:10]
    invoice['sender_iban'] = get_sender_iban(d.iban)

# print(tabulate(invoices))
print()

invoices = sorted(invoices, key=lambda k: k['sender_iban'])

for invoice in invoices:
    d = SimpleNamespace(**invoice)

    output = f'110,{d.date_due},{d.amount},{d.sender_iban[2:10]},0,'
    output += f'\"{d.sender_iban}\",\"{d.iban}\",'
    output += f'\"F.H. Domino|Henryk Szmek|ul. 1 Maja 60|43-460 Wisła\",'
    output += f'\"{d.issuer}\",0,{d.nrb},\"{d.invoice_number}\",'
    output += '\"\",'
    output += '\"\",'
    output += '\"51\"'
    print(output)
