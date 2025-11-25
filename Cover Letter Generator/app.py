import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Cover Letter Generator", page_icon="📝", layout="wide")

st.title("📝 Smart Cover Letter Generator")
st.markdown("Upload your resume and paste the job description to generate a tailored cover letter.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

def get_pdf_text(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    try:
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load_and_split()
        text = "".join([page.page_content for page in pages])
    finally:
        os.remove(temp_file_path)
    return text

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
    
    resume_text = ""
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = get_pdf_text(uploaded_file)
        else: # txt
            resume_text = uploaded_file.read().decode("utf-8")
        
        st.success("Resume uploaded and processed!")
        with st.expander("View Extracted Resume Text"):
            st.text(resume_text[:1000] + "...")

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area(
        "Paste the Job Description here",
        height=300,
        placeholder="Paste the full job description including requirements and responsibilities..."
    )

# Generate Button
if st.button("🚀 Generate Cover Letter", type="primary"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        st.stop()
        
    if not resume_text:
        st.error("Please upload your resume.")
        st.stop()
        
    if not job_description:
        st.error("Please provide the job description.")
        st.stop()

    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

    with st.spinner("Drafting your cover letter..."):
        try:
            template = """
            You are an expert career coach and professional writer.
            Please write a compelling cover letter based on the following:
            
            RESUME:
            {resume}
            
            JOB DESCRIPTION:
            {job_description}
            
            The cover letter should:
            1. Be professional and engaging.
            2. Highlight relevant skills and experiences from the resume that match the job description.
            3. Express enthusiasm for the role and company.
            4. Be formatted correctly as a formal letter.
            """
            
            prompt = PromptTemplate(template=template, input_variables=["resume", "job_description"])
            chain = prompt | llm
            response = chain.invoke({"resume": resume_text, "job_description": job_description})
            
            st.success("Cover Letter generated successfully!")
            st.markdown("### 📄 Generated Cover Letter")
            st.markdown("---")
            st.markdown(response.content)
            st.markdown("---")
            
            st.download_button(
                label="Download Cover Letter",
                data=response.content,
                file_name="cover_letter.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
