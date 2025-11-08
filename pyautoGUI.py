import pyautogui
import subprocess
import time
import os

# Safety feature: Set fail-safe to True (move mouse to top-left corner to abort)
pyautogui.FAILSAFE = True

# Step 1: Create the Python script (this is the script itself)

# Step 2: Open Safari browser
print("Opening Safari...")
subprocess.call(['open', '-a', 'Safari', 'https://web.whatsapp.com'])

# Give time for Safari to open and load WhatsApp Web
time.sleep(10)  # Adjust if needed; assumes already logged in (QR scanned previously)

# Step 3: Find/activate the WhatsApp Web tab/window
# Assuming Safari opens a new window/tab; focus on it
pyautogui.hotkey('command', 't')  # New tab if needed, but since we passed URL, it should be open
time.sleep(2)
pyautogui.hotkey('command', 'l')  # Focus on address bar, in case
time.sleep(1)
pyautogui.write('https://web.whatsapp.com')
pyautogui.press('enter')
time.sleep(10)  # Wait for page to load

# Step 4: Find the WhatsApp group "SE - AI-B3 - 2"
# Use search functionality in WhatsApp Web
print("Searching for group...")
pyautogui.hotkey('command', 'f')  # Open find (Cmd+F for search; fixed from press())
# WhatsApp Web search bar is usually at top; use image recognition or coordinates (brittle)
# For reliability, click approximate location of search bar (adjust coordinates for your screen)
# Assuming 1440x900 resolution; scale as needed. Use pyautogui.position() to find yours.
search_bar_x, search_bar_y = 400, 300  # Example: Top-leftish for search icon
pyautogui.click(search_bar_x, search_bar_y)
time.sleep(1)
#pyautogui.write('SE - AI-B3 - 2')
time.sleep(2)
pyautogui.press('enter')  # Select the first result (group)
time.sleep(3)  # Wait for chat to open

# Alternative: If search doesn't work, you can scroll through chats, but that's harder.

# Step 5: Write and send the message
print("Typing and sending message...")
message_box_x, message_box_y = 800, 820  # Example: Bottom message input area; adjust!
pyautogui.click(message_box_x, message_box_y)
time.sleep(1)
message = "I am sending a PyAutoGUI Validation message and task is completed"
pyautogui.write(message)
pyautogui.press('enter')  # Send
time.sleep(2)

# Step 6: Close the browser
print("Closing Safari...")
pyautogui.hotkey('command', 'w')  # Close tab
time.sleep(1)
pyautogui.hotkey('command', 'q')  # Quit Safari (optional; closes all windows)

print("Script completed!")