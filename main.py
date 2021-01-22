#!/usr/bin/env python3

from invoice import Invoice
from bundle import Bundle
import settings


def main():
    i = Invoice()
    data = i.get_processed_data()
    b = Bundle()

    # Create separate files split by sender IBAN
    for send_iban in settings.SENDER_IBAN:
        content = b.generate(data, send_iban)
        b.save_to_disk(send_iban, content)


if __name__ == '__main__':
    main()
