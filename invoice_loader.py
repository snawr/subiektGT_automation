import re
import os
from gui_automation import automation_sequence
from pdfminer.high_level import extract_text
from time import sleep
from datetime import datetime
import shutil

"""
TO MOŻESZ EDYTOWAĆ MACHIM
"""
base_sleep = 0.4
initial_countdown = 5


def remove_invalid_invoice_lines(text):
    text_list = (text.split('\n'))
    invalid_lines = ['', ' ', ' ']
    for line in text_list:
        if line in invalid_lines:
            text_list.remove(line)
    return text_list

def pdf_text_list_to_dict(text_list):
    text_dict = {}
    def add_to_dict(text_dict, key_val):
        text_dict[key_val[0]] = key_val[1]
        return text_dict

    value = None
    key = None
    key_val_pair = None
    for item in text_list:
        if item[-1]==':':
            if key and value:
                text_dict = add_to_dict(text_dict, [key, value])
                # print(f'text_dict {text_dict}')
            # print(f'key {item}')
            value = None
            key = item[:-1]
        elif ':' in item:
            if key and value:
                text_dict = add_to_dict(text_dict, [key, value])
                # print(f'text_dict {text_dict}')
            key_val_pair = item.split(':')
            # print(f'key_val {key_val_pair}')
            text_dict = add_to_dict(text_dict, key_val_pair)
            key = None
            value = None
        else:
            if value:
                value = value + ', ' + item
            else:
                if item[:7] == 'Faktura':
                    text_dict = add_to_dict(text_dict, ['nr_faktury', item])
                    continue

                value = item

            # print(f'value {value}')

        # print(f'key: {key}, value: {value}, pair: {key_val_pair}')
    # print(text_dict, newline='\n')
    # for key in text_dict:
    #     print(f'{key}: {text_dict[key]}')
    #     print(' ')
    return text_dict

def log_to_file(status, name, exception=None):
    with open('log.txt', 'a') as logfile:
        if status=='ok':
            logfile.write(f'{name} - OK   {datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}\n')
        else:
            logfile.write(f'{name} - FAIL   {datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}     - {exception}\n')

def move_file(name):
    shutil.move("./faktury/"+name, "./faktury_wrzucone/"+name)

if os.path.exists('log.txt'):
    os.remove('log.txt')

for sec in range(initial_countdown):
    print(f"startuje za {initial_countdown-sec}...")
    sleep(1)

with os.scandir('./faktury') as entries:
    for invoice_count, entry in enumerate(entries):
        print(str(invoice_count+1)+'. Ładuje plik: '+entry.name)

        text = extract_text("./faktury/"+entry.name)
        text_list = remove_invalid_invoice_lines(text)
        text_dict = pdf_text_list_to_dict(text_list)

        for key in text_dict:
            if key == 'nr_faktury':
                nr_faktury_lst = text_dict[key].split(' ')
                nr_faktury = nr_faktury_lst[2]
                print(nr_faktury)

            if key == 'Data sprzedaży':
                daty = text_dict[key].split(',')
                data_wystawienia = daty[0].strip()
                data_sprzedazy = daty[1].strip()
                print(data_wystawienia)
                print(data_sprzedazy)
            
            if key == 'Razem':
                wartosc_brutto = text_dict[key].split(' ')[0]
                print(wartosc_brutto) #string
 
        automation_sequence(nr_faktury, data_wystawienia.split('-'), data_sprzedazy.split('-'), wartosc_brutto.split('.')[0], base_sleep)
        log_to_file('ok', entry.name)
        move_file(entry.name)
        print('')

        # try:
        #     automation_sequence(nr_faktury, data_wystawienia.split('-'), data_sprzedazy.split('-'), wartosc_brutto.split('.')[0])
        #     log_to_file('ok', entry.name)
        #     move_file(entry.name)
        #     print('')
        # except Exception as e:
        #     print(e)
        #     log_to_file('fail', entry.name, exception=e)
        #     print('')

input("aby wyjść, naciśnij dowolny przycisk...")