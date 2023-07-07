import pyautogui
from time import sleep

def automation_steps(data):
    moveClick("help.png")
    sleep(1)
    # pyautogui.write(data)
    # pyautogui.hotkey("enter")

def moveClick(image):
    r= None 
    while r is None:
        r=pyautogui.locateCenterOnScreen('./img_lib/'+image,grayscale=False)
    # print(r)
    # pyautogui.moveTo(r)
    # sleep(1)
    pyautogui.click(r)



# res = pyautogui.locateOnScreen("help.png", confidence=.5)
# print(res)