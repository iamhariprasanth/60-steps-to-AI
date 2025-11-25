import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Smart Email Writer", page_icon="✉️", layout="centered")

st.title("✉️ Smart Email Writer")
st.markdown("Generate professional emails in seconds using AI. Just provide the context and choose your tone.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

# Main Interface
col1, col2 = st.columns([3, 1])

with col1:
    email_context = st.text_area(
        "Email Context",
        placeholder="E.g., I need to ask my boss for a leave next Friday because I have a dentist appointment.",
        height=150
    )

with col2:
    tone = st.selectbox(
        "Select Tone",
        ["Professional", "Expert", "Friendly", "Casual", "Urgent", "Apologetic"]
    )

# Generate Button
if st.button("✨ Generate Email", type="primary"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        st.stop()
        
    if not email_context:
        st.error("Please provide the context for the email.")
        st.stop()

    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

    with st.spinner("Drafting your email..."):
        try:
            template = """
            You are an expert email writer.
            Please write a {tone} email based on the following context:
            
            Context:
            {context}
            
            The email should be well-structured, clear, and ready to send. 
            Subject line should be included.
            """
            
            prompt = PromptTemplate(template=template, input_variables=["tone", "context"])
            chain = prompt | llm
            response = chain.invoke({"tone": tone, "context": email_context})
            
            st.success("Email generated successfully!")
            st.markdown("### 📧 Generated Email")
            st.markdown("---")
            st.markdown(response.content)
            st.markdown("---")
            
            # Copy button (simulated via code block for now as Streamlit native copy is limited)
            st.caption("You can copy the email content from above.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
