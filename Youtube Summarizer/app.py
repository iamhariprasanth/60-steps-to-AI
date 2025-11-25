import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from dotenv import load_dotenv
import os
import yt_dlp
import openai
import tempfile

# Load environment variables
load_dotenv()

st.set_page_config(page_title="YouTube Summarizer", page_icon="📺", layout="wide")

st.title("📺 YouTube Video Summarizer")
st.markdown("Get concise summaries of YouTube videos, even if they don't have transcripts!")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

def download_audio(url):
    """Downloads audio from YouTube video using yt-dlp without requiring ffmpeg."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_file:
        temp_filename = temp_file.name

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',  # Prefer m4a which doesn't need conversion
        'outtmpl': temp_filename,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if file exists
        if os.path.exists(temp_filename):
            return temp_filename
        # Sometimes yt-dlp adds extension
        elif os.path.exists(temp_filename + ".m4a"):
            return temp_filename + ".m4a"
        elif os.path.exists(temp_filename + ".webm"):
            return temp_filename + ".webm"
        else:
            raise Exception("Downloaded file not found")
    except Exception as e:
        raise Exception(f"Failed to download audio: {e}")

def transcribe_audio(audio_path, api_key):
    """Transcribes audio using OpenAI Whisper."""
    client = openai.OpenAI(api_key=api_key)
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript.text

def get_video_transcript(url, api_key):
    """Orchestrates transcript retrieval: API first, then Whisper fallback."""
    # Try fetching transcript via API with multiple language options
    transcript_found = False
    transcript_text = None
    
    # Try common languages
    languages_to_try = [
        ["en", "en-US", "en-GB"],  # English
        ["es", "es-ES"],  # Spanish
        ["fr", "fr-FR"],  # French
        ["de", "de-DE"],  # German
        ["hi", "hi-IN"],  # Hindi
        ["ta", "ta-IN"],  # Tamil
    ]
    
    for lang_list in languages_to_try:
        try:
            loader = YoutubeLoader.from_youtube_url(
                url, 
                add_video_info=False,
                language=lang_list
            )
            docs = loader.load()
            transcript_text = docs[0].page_content
            transcript_found = True
            st.info(f"Found transcript in language: {lang_list[0]}")
            break
        except Exception:
            continue
    
    if not transcript_found:
        st.warning("No transcript found in any language. Attempting to transcribe audio (this may take a moment)...")
        
        try:
            audio_path = download_audio(url)
            transcript_text = transcribe_audio(audio_path, api_key)
            # Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as inner_e:
            raise Exception(f"Failed to transcribe video: {inner_e}")
    
    return transcript_text

# Main Interface
video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("📝 Summarize Video", type="primary"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        st.stop()
        
    if not video_url:
        st.error("Please provide a valid YouTube URL.")
        st.stop()

    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

    with st.spinner("Processing video..."):
        try:
            # 1. Get Transcript
            transcript_text = get_video_transcript(video_url, api_key)
            
            # 2. Summarize
            with st.spinner("Generating summary..."):
                template = """
                You are a helpful assistant that summarizes YouTube videos.
                Please provide a concise and informative summary of the following video transcript:
                
                Transcript:
                {transcript}
                
                Summary:
                """
                
                # Handle long transcripts by truncating or using a map-reduce chain (simplified here for MVP)
                # GPT-4o has 128k context, so we can handle reasonably long videos (approx 2-3 hours of speech).
                # We'll truncate to 100k chars to be safe.
                if len(transcript_text) > 100000:
                    transcript_text = transcript_text[:100000] + "...(truncated)"
                
                prompt = PromptTemplate(template=template, input_variables=["transcript"])
                chain = prompt | llm
                response = chain.invoke({"transcript": transcript_text})
                
                st.success("Summary generated successfully!")
                st.markdown("### 📋 Video Summary")
                st.markdown("---")
                st.markdown(response.content)
                st.markdown("---")
                
                with st.expander("View Transcript"):
                    st.text(transcript_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
