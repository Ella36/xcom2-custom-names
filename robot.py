# Disabl numlock
import pyautogui
import time
from time import sleep

# 1080p coordinates of rows
row_y = [221, 257, 296, 337, 372, 414, 450, 490, 527, 566, 604]

time.sleep(3)


def function():
    # Click character start
    pyautogui.click()

    # Character info
    pyautogui.moveTo(407, 334, duration=2)
    pyautogui.click()
    pyautogui.click()
    sleep(1)
    pyautogui.click()
    pyautogui.click()
    sleep(1)

    # First name
    pyautogui.moveTo(403, 330, duration=2)
    pyautogui.typewrite(".")
    sleep(1)

    # confirm
    pyautogui.click()
    pyautogui.moveTo(1073, 593, duration=2)
    pyautogui.click()

    # last name
    pyautogui.moveTo(384, 371, duration=1)
    pyautogui.click()
    sleep(1)
    pyautogui.typewrite("tomaxlengthname")
    # confirm
    pyautogui.moveTo(1065, 602, duration=1)
    sleep(1)
    pyautogui.click()

    # nickname
    pyautogui.moveTo(370, 410, duration=1)
    sleep(1)
    pyautogui.click()
    sleep(1)
    pyautogui.press("delete")
    pyautogui.moveTo(1065, 602, duration=1)
    pyautogui.click()
    sleep(1)
    # Reset to pool
    pyautogui.moveTo(54, 1037, duration=1)
    sleep(1)
    pyautogui.click()
    pyautogui.moveTo(55, 1030, duration=1)
    sleep(1)
    pyautogui.click()


while True:
    for y in row_y:
        # Move next row
        pyautogui.moveTo(358, y, duration=2)  # top row + adjust
        function()
    pyautogui.moveTo(624, 784, duration=5)  # bottom reset
    pyautogui.click()
