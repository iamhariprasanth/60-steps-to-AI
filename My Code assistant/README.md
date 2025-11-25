# My Code Assistant

An AI-powered assistant to help you generate code and fix errors in various programming languages.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation
1. Navigate to the directory:
   ```bash
   cd "My Code assistant"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (optional):
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```
   - Alternatively, you can enter the API key in the app's sidebar.

## How to Run
```bash
streamlit run app.py
```

## Usage
1. **Enter API Key**: Provide your OpenAI API Key in the sidebar.
2. **Select Language**: Choose your programming language (Python, JS, etc.).
3. **Select Task**:
   - **Generate Code**: Describe what you want the code to do.
   - **Fix Error**: Paste your buggy code and the error message.
4. Click **Run Assistant** to get the result.
