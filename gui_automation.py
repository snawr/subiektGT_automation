import pyautogui
from time import sleep


def automation_sequence(nr_faktury, data_wystawienia, data_sprzedazy, wartosc_brutto, base_sleep):
    moveClick("wykonaj.png")
    sleep(base_sleep)

    # numer faktury
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write(nr_faktury)
    sleep(base_sleep)

    # Data wystawienia i sprzedaży
    pyautogui.press('tab')
    for i in range(3):
        pyautogui.press('tab')
        for j in range(3):
            if i!=1:
                pyautogui.write(data_sprzedazy[j])
            else:
                pyautogui.write(data_wystawienia[j])
        sleep(0.1)

    # wartosc brutto
    moveClick("wartosc_brutto.png")
    # wartosc_brutto = '7'
    pyautogui.write(wartosc_brutto)
    pyautogui.press('tab')

    # zaplacono przelewem
    pyautogui.hotkey('ctrl', '4')
    sleep(base_sleep)
    # zapisz
    moveClick("zapisz.png")

    sleep(1)


def moveClick(image):
    r= None 
    for _ in range(5):
        try:
            r=pyautogui.locateCenterOnScreen('./img_lib/'+image,grayscale=False)
            if r:
                break
        except pyautogui.ImageNotFoundException:
                sleep(0.5)
                print(f'nie znalazło {image}, próbuje jeszcze raz')

    # print(r)
    # pyautogui.moveTo(r)
    # sleep(1)
    pyautogui.click(r)
