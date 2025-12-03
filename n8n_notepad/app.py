#!/usr/bin/env python3
"""
Flask API to open Notepad (TextEdit on macOS), write input from payload, and save to a file.
Filename: n8nnotepad_demo.txt
- If file doesn't exist, create it
- If file exists, append new input on a new line
"""

from flask import Flask, request, jsonify
import pyautogui
import time
import os
import subprocess
import pyperclip

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Simple landing route to list available endpoints."""
    return jsonify({
        "message": "Notepad Writer API is running",
        "available_endpoints": {
            "POST /write": "Write text (payload: {'text': 'your text'})",
            "GET /read": "Read file content",
            "DELETE /clear": "Delete the file",
            "GET /health": "Health check"
        }
    }), 200

# Configuration
FILENAME = "n8nnotepad_demo.txt"
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


def write_to_file(text):
    """Write/append text to the file directly."""
    os.makedirs(os.path.dirname(FILE_PATH) or '.', exist_ok=True)
    
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


@app.route('/write', methods=['POST'])
def write_to_notepad():
    """
    API endpoint to write text to notepad.
    
    Expects JSON payload:
    {
        "text": "Your text here"
    }
    """
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON payload provided"
            }), 400
        
        # Get text from payload
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided in payload. Use {'text': 'your text'}"
            }), 400
        
        # Write to file
        had_content = write_to_file(text)
        
        # Open in TextEdit for visual confirmation
        open_and_display_in_textedit()
        
        return jsonify({
            "success": True,
            "message": f"Text {'appended' if had_content else 'written'} successfully",
            "text": text,
            "file_path": FILE_PATH
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/read', methods=['GET'])
def read_notepad():
    """
    API endpoint to read the current content of the notepad file.
    """
    try:
        if not os.path.exists(FILE_PATH):
            return jsonify({
                "success": False,
                "error": "File does not exist yet"
            }), 404
        
        with open(FILE_PATH, 'r') as f:
            content = f.read()
        
        return jsonify({
            "success": True,
            "content": content,
            "file_path": FILE_PATH
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/clear', methods=['DELETE'])
def clear_notepad():
    """
    API endpoint to clear/delete the notepad file.
    """
    try:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)
            return jsonify({
                "success": True,
                "message": "File deleted successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "File does not exist"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "file_path": FILE_PATH
    }), 200


if __name__ == '__main__':
    print("=" * 50)
    print("Notepad Writer Flask API")
    print("=" * 50)
    print(f"File path: {FILE_PATH}")
    print("Endpoints:")
    print("  POST /write  - Write text (payload: {'text': 'your text'})")
    print("  GET  /read   - Read file content")
    print("  DELETE /clear - Clear/delete file")
    print("  GET  /health - Health check")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=False)
