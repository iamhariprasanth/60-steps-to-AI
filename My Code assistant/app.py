import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="My Code Assistant", page_icon="💻", layout="wide")

st.title("💻 My Code Assistant")
st.markdown("Generate code or fix errors in your favorite programming languages using Gen AI.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Select Programming Language",
        ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript", "Swift", "Kotlin", "SQL", "HTML/CSS", "Bash"]
    )

with col2:
    task_type = st.selectbox(
        "Select Task",
        ["Generate Code", "Fix Error"]
    )

# Dynamic Inputs based on Task
if task_type == "Generate Code":
    st.subheader(f"Generate {language} Code")
    problem_description = st.text_area("Describe the problem or functionality you need:", height=200)
    code_input = None
    error_input = None
else:
    st.subheader(f"Fix {language} Error")
    code_input = st.text_area("Paste your code here:", height=200)
    error_input = st.text_area("Paste the error message here:", height=100)
    problem_description = None

# Submit Button
if st.button("🚀 Run Assistant"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        st.stop()

    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

    with st.spinner("Processing..."):
        try:
            if task_type == "Generate Code":
                if not problem_description:
                    st.error("Please describe the problem.")
                    st.stop()
                
                template = """
                You are an expert programmer in {language}.
                Please write clean, efficient, and well-commented code to solve the following problem:
                
                Problem:
                {problem}
                
                Provide the code and a brief explanation of how it works.
                """
                prompt = PromptTemplate(template=template, input_variables=["language", "problem"])
                chain = prompt | llm
                response = chain.invoke({"language": language, "problem": problem_description})
                
            else: # Fix Error
                if not code_input or not error_input:
                    st.error("Please provide both code and the error message.")
                    st.stop()
                
                template = """
                You are an expert programmer in {language}.
                I have the following code which is causing an error.
                
                Code:
                {code}
                
                Error:
                {error}
                
                Please analyze the error, fix the code, and explain what was wrong and how you fixed it.
                """
                prompt = PromptTemplate(template=template, input_variables=["language", "code", "error"])
                chain = prompt | llm
                response = chain.invoke({"language": language, "code": code_input, "error": error_input})

            # Display Result
            st.success("Done!")
            st.markdown("### Result")
            st.markdown(response.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")

