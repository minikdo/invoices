#!/usr/bin/env python3

import os
import sys
from types import SimpleNamespace
from typing import List, Dict
from datetime import datetime, timedelta
from string import Template

from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

from splitamount import SplitAmount
import settings
import iban_map


class FileManager:

    INVOICE_DIR = settings.INVOICE_DIR

    def __init__(self):
        pass

    def get_pdf_list(self) -> List[str]:
        pdfs = []
        for file in os.listdir(self.INVOICE_DIR):
            _, ext = os.path.splitext(file)
            if 'pdf' in ext:
                pdfs.append(os.path.join(self.INVOICE_DIR, file))
        return pdfs

    def read_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except OSError as e:
            print('Error:', e)
            sys.exit(1)

    def write_data(self, filename, content):
        try:
            with open(filename, "w") as file:
                file.write(content)
                print("{} written".format(filename))
        except OSError as e:
            print('Error:', e)
            sys.exit(1)


class Invoice:

    fm = FileManager()

    def __init__(self):
        pass

    def read_templates(self):
        return read_templates(settings.TEMPLATE_DIR)

    def parse_pdfs(self) -> List[Dict]:
        result = []
        pdf_list = self.fm.get_pdf_list()
        templates = self.read_templates()

        for pdf in pdf_list:
            data = extract_data(pdf, templates=templates)
            result.append(data)
        return result

    def get_sender(self, iban):
        for key, value in iban_map.SENDER_IBAN_MAP.items():
            if iban in value:
                return iban_map.SENDER_IBAN[key]
                # raise Exception("IBAN {} is missing".format(iban))

    def process_fields(self, data):
        d = SimpleNamespace(**data)

        data['date'] = d.date.strftime('%Y%m%d')
        data['amount'] = SplitAmount(d.amount).get_full_amount()
        data['recv_iban'] = d.iban[2:10]
        data['send_iban'] = self.get_sender(d.iban)
        data['send_iban_short'] = data['send_iban'][2:10]

        # Some invoices provide full date, others - number of days left
        if 'days_due' in data.keys():
            data['date_due'] = d.date + timedelta(days=int(d.days_due))
        else:
            data['date_due'] = d.date_due.strftime('%Y%m%d')

        return data

    def get_processed_data(self):
        result = []
        pdfs_data = self.parse_pdfs()
        for data in pdfs_data:
            result.append(self.process_fields(data))
        return result


class Bundle:

    fm = FileManager()

    def __init__(self):
        pass

    def get_template(self):
        return self.fm.read_data('template.pli')

    def filter_data(self, data, send_iban):
        """Returns a generator filtered by the sender IBAN."""
        return (d for d in data if d['send_iban'] == send_iban)

    def generate(self, data, send_iban):
        """Generates a bundle."""
        content = self.get_template()
        template = Template(content)
        sender = iban_map.SENDER
        result = ''
        for item in self.filter_data(data, send_iban):
            result += template.substitute(sender=sender, **item)
        return result

    def save_to_disk(self, send_iban, content):
        """Saves a bundle to disk."""
        filename = "{}-{}.pli".format(send_iban,
                                      datetime.now().strftime("%Y%m%d-%H%M%S"))
        filename = os.path.join(settings.BUNDLE_DIR, filename)
        self.fm.write_data(filename, content)


def main():
    i = Invoice()
    data = i.get_processed_data()
    b = Bundle()

    # Create separate files split by sender IBAN
    for send_iban in iban_map.SENDER_IBAN:
        content = b.generate(data, send_iban)
        b.save_to_disk(send_iban, content)


if __name__ == '__main__':
    main()
