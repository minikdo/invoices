from typing import Dict, Generator, Any
from string import Template

from filemanager import FileManager
import settings


class Bundle:

    fm = FileManager()

    def __init__(self):
        pass

    def get_template(self) -> str:
        return self.fm.read_data('template.pli')

    def filter_data(self, data: Dict,
                    send_iban: str) -> Generator[Dict[str, Any], None, None]:
        """Returns a generator filtered by the sender IBAN."""
        return (d for d in data if d['send_iban'] == send_iban)

    def generate(self, data, send_iban: str) -> str:
        """Generates a bundle."""
        content = self.get_template()
        template = Template(content)
        sender = settings.SENDER
        result = ''
        for item in self.filter_data(data, send_iban):
            result += template.substitute(sender=sender, **item)
        return result

    def save_to_disk(self, send_iban: str, content: str) -> None:
        """Saves a bundle to disk."""
        self.fm.write_data(send_iban, content)
