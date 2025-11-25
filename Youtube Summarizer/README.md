# YouTube Summarizer

Get concise summaries of YouTube videos, using official transcripts or AI-powered audio transcription.

## Prerequisites
- Python 3.8+
- OpenAI API Key
- **FFmpeg**: Required for audio processing if falling back to Whisper.
    - Mac: `brew install ffmpeg`

## Installation
1. Navigate to the directory:
   ```bash
   cd "Youtube Summarizer"
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
2. **Video URL**: Paste the link to the YouTube video you want to summarize.
3. Click **Summarize Video**.
4. The app will first try to fetch existing captions. If none exist, it will download the audio and transcribe it using OpenAI Whisper (this takes longer).
