# Smart Email Writer

Generate professional, tailored emails in seconds using AI.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation
1. Navigate to the directory:
   ```bash
   cd "Smart Email Writer"
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
2. **Email Context**: Describe the purpose of the email (e.g., "Asking for a sick leave").
3. **Select Tone**: Choose a tone (Professional, Friendly, Urgent, etc.).
4. Click **Generate Email**.
5. Copy the generated subject and body.
