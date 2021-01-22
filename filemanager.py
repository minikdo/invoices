import os
import sys
from typing import List
from datetime import datetime

import settings


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

    def create_filename(self, send_iban: str) -> str:
        filename = "{}-{}.pli".format(datetime.now().strftime("%Y%m%d-%H%M%S"),
                                      send_iban)
        return os.path.join(settings.BUNDLE_DIR, filename)

    def read_data(self, filename: str) -> str:
        try:
            with open(filename, 'r') as file:
                return file.read()
        except OSError as e:
            print('Error:', e)
            sys.exit(1)

    def write_data(self, send_iban: str, content: str) -> None:
        filename = self.create_filename(send_iban)
        try:
            with open(filename, "w") as file:
                file.write(content)
                print("{} written".format(filename))
        except OSError as e:
            print('Error:', e)
            sys.exit(1)
