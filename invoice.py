from typing import List, Dict
from datetime import timedelta
from types import SimpleNamespace

from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

from splitamount import SplitAmount
from filemanager import FileManager
import settings


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

    def get_sender(self, iban: str) -> str:
        for key, value in settings.SENDER_IBAN_MAP.items():
            if iban in value:
                return key

        raise Exception(f"IBAN {iban} is missing")
        return ''

    def process_fields(self, data: Dict) -> Dict:
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

    def get_processed_data(self) -> List[Dict]:
        result = []
        pdfs_data = self.parse_pdfs()
        for data in pdfs_data:
            result.append(self.process_fields(data))
        return result
