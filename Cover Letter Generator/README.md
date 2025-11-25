# Cover Letter Generator

Create tailored cover letters based on your resume and a job description.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation
1. Navigate to the directory:
   ```bash
   cd "Cover Letter Generator"
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
2. **Upload Resume**: Upload your resume in PDF or TXT format.
3. **Job Description**: Paste the job description you are applying for.
4. Click **Generate Cover Letter**.
5. You can view the result on screen or download it as a markdown file.
