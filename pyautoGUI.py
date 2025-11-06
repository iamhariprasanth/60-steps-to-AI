import time
import pyautogui

## Mouse Operations
pyautogui.click(x=100, y=200)  # Click at coordinates (100, 200)
time.sleep(10)
pyautogui.doubleClick(x=150, y=250)  # Double click at
# time.sleep(10)
# pyautogui.rightClick(x=200, y=300)  # Right click at
# time.sleep(10)
# pyautogui.moveTo(x=300, y=400, duration=1)
# time.sleep(10)
# pyautogui.moveRel(xOffset=100, yOffset=0, duration=1
# )  # Move right by 100 pixels
# time.sleep(10)
# pyautogui.dragTo(x=400, y=500, duration=1)
# time.sleep(10)
# pyautogui.typewrite('Hello, World!', interval=0.1)  # Type text with a delay between each character
# time.sleep(10)
# pyautogui.press('enter')  # Press the Enter key
time.sleep(10)
pyautogui.hotkey('ctrl', 's')  # Press Ctrl+S to save the file  
pyautogui.locateAllOnScreen('copilot.png')  # Locate all instances of an image on the screen