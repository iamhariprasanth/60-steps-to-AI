# Mock Interview Assistant

Generate context-specific interview questions and answers based on your target role and tech stack.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation
1. Navigate to the directory:
   ```bash
   cd "Mock Interview Assistant"
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
2. **Job Role**: Enter the role you are applying for (e.g., "Senior Python Developer").
3. **Tech Stack**: Enter the tools and technologies (e.g., "Django, AWS, Docker").
4. **Experience**: Select your years of experience.
5. Click **Generate Questions** to get the first 10 questions.
6. Click **Generate More** to append 5 more questions.
