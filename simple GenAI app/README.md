# Simple GenAI App

A basic Generative AI application using LangChain and OpenAI.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation
1. Navigate to the directory:
   ```bash
   cd "simple GenAI app"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## How to Run
```bash
streamlit run app.py
```

## Usage
1. Enter your query in the text input field.
2. The AI will generate a response based on your input.
