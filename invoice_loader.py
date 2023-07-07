import re
import os
from gui_automation import automation_steps
from pdfminer.high_level import extract_text

def automate_gui():
    pass

pattern = re.compile(r"\d{4}-\d\d-\d\d")


with os.scandir('./faktury') as entries:
    for invoice_count, entry in enumerate(entries):
        print(str(invoice_count+1)+'. Ładuje plik: '+entry.name)

        text = extract_text("./faktury/"+entry.name)
        # print(text)
        matches = pattern.finditer(text)

        for match_count, match in enumerate(matches):
            if match_count==0:
                data_wyst = match.group()
                print('Data wystawienia: '+data_wyst)
            if match_count==1:
                data_sprz = match.group()
                print('Data sprzedaży: '+data_sprz)
        automation_steps(data_sprz)
        print(' ')


