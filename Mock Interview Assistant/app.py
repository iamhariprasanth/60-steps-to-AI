import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Mock Interview Assistant", page_icon="🎤", layout="wide")

st.title("🎤 Mock Interview Assistant")
st.markdown("Generate context-specific interview questions and answers based on your target role and tech stack.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here if not set in environment variables.")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

# Initialize Session State
if "questions" not in st.session_state:
    st.session_state.questions = []

# Main Interface
col1, col2 = st.columns(2)

with col1:
    role = st.text_input("Job Role", placeholder="e.g. Senior Python Developer")

with col2:
    tools = st.text_input("Tech Stack / Tools", placeholder="e.g. Django, AWS, Docker, PostgreSQL")

experience = st.slider("Years of Experience", 0, 20, 3)

def generate_questions(num_questions=10):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
        return

    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
    
    with st.spinner(f"Generating {num_questions} interview questions..."):
        try:
            # Context for previous questions to avoid duplicates (simplified)
            existing_topics = [q['question'] for q in st.session_state.questions]
            existing_context = "\n".join(existing_topics[-20:]) # Keep last 20 to avoid context limit issues
            
            template = """
            You are an expert technical interviewer.
            Generate {num_questions} interview questions and answers for a candidate applying for the following role:
            
            Role: {role}
            Tech Stack: {tools}
            Experience: {experience} years
            
            The questions must be:
            1. Specific to the tools and context provided.
            2. Not generic behavioral questions (unless highly relevant to a senior role).
            3. Challenging and appropriate for the experience level.
            
            Format the output strictly as a list of Q&A pairs. 
            Use "Q:" for Question and "A:" for Answer.
            Separate each pair with a double newline.
            
            Avoid repeating these questions:
            {existing_context}
            """
            
            prompt = PromptTemplate(template=template, input_variables=["num_questions", "role", "tools", "experience", "existing_context"])
            chain = prompt | llm
            response = chain.invoke({
                "num_questions": num_questions, 
                "role": role, 
                "tools": tools, 
                "experience": experience,
                "existing_context": existing_context
            })
            
            # Parse response
            content = response.content
            pairs = content.split("\n\n")
            new_questions = []
            current_q = ""
            current_a = ""
            
            for part in pairs:
                if "Q:" in part and "A:" in part:
                    # Simple parsing, might need robustness for complex LLM outputs
                    try:
                        q_part, a_part = part.split("A:", 1)
                        q_clean = q_part.replace("Q:", "").strip()
                        a_clean = a_part.strip()
                        new_questions.append({"question": q_clean, "answer": a_clean})
                    except ValueError:
                        continue
                elif part.strip().startswith("Q:"):
                     # Handle case where split might have failed or format is slightly different
                     pass 

            # Fallback if simple parsing fails, just dump the text (or improve parsing)
            # For this demo, let's assume the LLM follows instructions well enough or we just display raw if needed.
            # Actually, let's just store the raw text blocks if parsing is too brittle, 
            # but let's try to be structured.
            
            if not new_questions:
                 # If structured parsing failed, let's just try to split by "Q:"
                 raw_splits = content.split("Q:")
                 for split in raw_splits:
                     if "A:" in split:
                         q_part, a_part = split.split("A:", 1)
                         new_questions.append({"question": q_part.strip(), "answer": a_part.strip()})

            st.session_state.questions.extend(new_questions)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Buttons
col_btn1, col_btn2 = st.columns([1, 4])

with col_btn1:
    if st.button("🚀 Generate Questions", type="primary"):
        st.session_state.questions = [] # Reset on new generation
        if not role or not tools:
            st.error("Please provide both Role and Tech Stack.")
        else:
            generate_questions(10)

with col_btn2:
    if st.session_state.questions:
        if st.button("➕ Generate More"):
             generate_questions(5)

# Display Questions
if st.session_state.questions:
    st.markdown("### 📝 Interview Questions")
    for i, qa in enumerate(st.session_state.questions):
        with st.expander(f"Q{i+1}: {qa['question']}"):
            st.markdown(f"**Answer:**\n{qa['answer']}")
            
