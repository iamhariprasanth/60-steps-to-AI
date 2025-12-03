#!/usr/bin/env python3
"""
PyAutoGUI script to open Notepad (TextEdit on macOS), write user input, and save to a file.
Filename: socialeagleaidemo.txt
- If file doesn't exist, create it
- If file exists, append new input on a new line
"""

import pyautogui
import time
import os
import sys
import subprocess
import pyperclip

# Configuration
FILENAME = "n8nnotepad_demo.txt"
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


def get_user_input():
    """Get input from command line arguments or prompt user."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    else:
        return input("Enter the text to write to notepad: ")


def write_to_file(text):
    """Write/append text to the file directly."""
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    # Check if file exists and has content
    file_has_content = os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0
    
    # Append or write
    mode = 'a' if file_has_content else 'w'
    with open(FILE_PATH, mode) as f:
        if file_has_content:
            f.write('\n')
        f.write(text)
    
    return file_has_content


def open_and_display_in_textedit():
    """Open the file in TextEdit and display the content."""
    # Close TextEdit if open
    subprocess.run(['osascript', '-e', 'tell application "TextEdit" to quit'], 
                   capture_output=True, timeout=5)
    time.sleep(1)
    
    # Open file in TextEdit
    subprocess.Popen(['open', '-a', 'TextEdit', FILE_PATH])
    time.sleep(2)
    
    # Activate TextEdit and bring to front
    subprocess.run(['osascript', '-e', 'tell application "TextEdit" to activate'])
    time.sleep(1)
    
    # Click to focus the document
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(0.5)
    
    # Go to end of document to show new content
    pyautogui.hotkey('command', 'down')
    time.sleep(0.3)
    
    # Save the document (Cmd+S)
    pyautogui.hotkey('command', 's')
    time.sleep(0.5)
    
    # Close TextEdit after saving
    subprocess.run(['osascript', '-e', 'tell application "TextEdit" to quit'])
    time.sleep(0.5)


def main():
    """Main function to orchestrate the notepad writing process."""
    print("=" * 50)
    print("Notepad Writer Script")
    print("=" * 50)
    
    # Get user input
    user_text = get_user_input()
    
    if not user_text.strip():
        print("Error: No text provided. Exiting.")
        sys.exit(1)
    
    print(f"Text to write: '{user_text}'")
    
    # Write directly to file (reliable method)
    print("Writing to file...")
    had_content = write_to_file(user_text)
    print(f"File {'appended' if had_content else 'created'}: {FILE_PATH}")
    
    # Open in TextEdit for visual confirmation
    print("Opening TextEdit...")
    open_and_display_in_textedit()
    
    print("=" * 50)
    print("Done!")
    print(f"File saved at: {FILE_PATH}")
    print("=" * 50)


if __name__ == "__main__":
    main()
