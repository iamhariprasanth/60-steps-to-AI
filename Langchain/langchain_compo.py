# rag_openai_faiss.py
# Install (one time, in your virtual environment):
#   pip install -U langchain langchain-openai langchain-community faiss-cpu tiktoken

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# OpenAI integration for embeddings and chat
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# FAISS vectorstore adapter (community)
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---- Config ----
# Set your OpenAI API key in environment:
#   export OPENAI_API_KEY="sk-..." (macOS/Linux)
#   setx OPENAI_API_KEY "sk-..." (Windows, then restart VSCode/terminal)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable before running.")

# ---- 1) Load documents ----
# Update this path to point to your actual PDF file
PDF_PATH = "/Users/hariprasanthmadhavan/60-steps-to-AI/Langchain/report.pdf"
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()  # returns list[Document]

# ---- 2) Preprocess / split ----
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(docs)  # list[Document] (smaller pieces)

# ---- 3) Create embeddings (OpenAI) ----
embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY

# ---- 4) Build FAISS vectorstore ----
vectorstore = FAISS.from_documents(chunks, embeddings)

# ---- 5) Create retriever from vectorstore ----
# You can pass search kwargs: e.g., search_kwargs={"k": 4}
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---- 6) Prepare LLM (ChatOpenAI) ----
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=500)

# ---- 7) Define prompt template ----
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the following documents to answer the question."),
    ("user", "Documents:\n{context}\n\nQuestion: {query}\n\nAnswer succinctly."),
])

# ---- 8) Create simple LCEL chain: prompt | LLM | parser ----
chain = prompt | llm | StrOutputParser()

# ---- 9) Run a query using retriever + chain ----
query = "What are the main findings and recommendations in the report?"
# Get top documents
docs_out = retriever.invoke(query)
docs_text = "\n\n".join([d.page_content for d in docs_out])

# Invoke the chain
answer = chain.invoke({"context": docs_text, "query": query})
print("Answer:\n", answer)

# Optional: Save the vectorstore for reuse (e.g., in another script)
# vectorstore.save_local("faiss_index")
# To load later: vectorstore = FAISS.load_local("faiss_index", embeddings)

# Optional: inspect sources / doc metadata returned by retriever
# for d in docs_out[:3]:
#     print(d.metadata)