import streamlit as st
import fitz
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Load environment variables
load_dotenv()

# Gemini setup
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ChromaDB setup
@st.cache_resource
def get_chroma_client():
    return chromadb.PersistentClient(path="./chroma_db")

client = get_chroma_client()

collection = client.get_or_create_collection(
    name="pdf_collection"
)

# Session state
if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# UI
st.title("📄 PDF AI Chatbot")

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

# Process PDFs
if uploaded_files and not st.session_state.processed:
    with st.spinner("Processing PDFs..."):
        try:
            existing = collection.get()
            if existing["ids"]:
                collection.delete(
                    ids=existing["ids"]
                )
        except Exception:
            pass

        documents = []

        for uploaded_file in uploaded_files:
            pdf = fitz.open(
                stream=uploaded_file.read(),
                filetype="pdf"
            )

            for page_num, page in enumerate(pdf):
                text = page.get_text()
                if text.strip():
                    documents.append(
                        {
                            "text": text,
                            "page": page_num + 1,
                            "source": uploaded_file.name
                        }
                    )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = []

        for doc in documents:
            split_texts = splitter.split_text(
                doc["text"]
            )
            for chunk in split_texts:
                chunks.append(
                    {
                        "text": chunk,
                        "page": doc["page"],
                        "source": doc["source"]
                    }
                )

        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[str(i)],
                documents=[chunk["text"]],
                metadatas=[
                    {
                        "page": chunk["page"],
                        "source": chunk["source"]
                    }
                ]
            )

        st.session_state.processed = True
        st.success(
            f"{len(uploaded_files)} PDF(s) processed successfully."
        )

# Ask Questions
if st.session_state.processed:
    question = st.chat_input(
        "Ask a question about the uploaded PDFs..."
    )

    if question:
        with st.spinner("Searching documents..."):
            results = collection.query(
                query_texts=[question],
                n_results=5
            )
            context = "\n\n".join(
                results["documents"][0]
            )

        with st.spinner("Generating answer..."):
            prompt = f"""
Answer ONLY using the provided context.

Format the answer using bullet points and headings.

If the answer is not found, reply:
Information not found in uploaded documents.

Context:
{context}

Question:
{question}
"""
            response = model.generate_content(
                prompt
            )
            answer = response.text

        st.subheader("Answer")
        st.markdown(answer)

        st.subheader("Source Pages")

        unique_pages = []

        for meta in results["metadatas"][0]:
            page_info = (
                f"{meta['source']} - Page {meta['page']}"
            )
            if page_info not in unique_pages:
                unique_pages.append(page_info)

        for page in unique_pages:
            st.write(f"• {page}")

        st.subheader("Source Excerpts")

        for doc in results["documents"][0]:
            st.info(doc[:400] + "...")

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

# Chat History
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Chat History")

    for item in reversed(st.session_state.chat_history):
        st.write(f"**Question:** {item['question']}")
        st.write(f"**Answer:** {item['answer']}")
        st.markdown("---")