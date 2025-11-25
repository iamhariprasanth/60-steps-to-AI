import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Simple Gen AI Chat", page_icon="🤖")

st.title("🤖 Simple Gen AI Chat")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat Input
if prompt := st.chat_input("What is up?"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        st.stop()

    # Add user message to history
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
        
        with st.chat_message("assistant"):
            response = llm.invoke(st.session_state.messages)
            st.markdown(response.content)
        
        st.session_state.messages.append(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
