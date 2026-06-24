# 📄 PDF AI Chatbot

An AI-powered PDF Question Answering chatbot built using Python, Streamlit, Google Gemini AI, and ChromaDB. Users can upload PDF documents and ask questions based on the content of the uploaded files.

## 🚀 Features

- Upload one or more PDF files
- Extract text from PDFs using PyMuPDF
- Split large documents into chunks
- Store document chunks in ChromaDB
- Semantic search for relevant content
- AI-powered answers using Google Gemini
- Display source pages and excerpts
- Chat history support
- Deployed on Streamlit Cloud

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & LLM
- Google Gemini API

### Vector Database
- ChromaDB

### Document Processing
- PyMuPDF (fitz)

### Text Processing
- LangChain Text Splitters

---

## 📂 Project Structure

```text
pdf-chatbot/
│
├── app.py
├── requirements.txt
├── .gitignore
├── chroma_db/
├── README.md
└── .env
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/karthiktcs387/pdf-ai-chatbot.git
cd pdf-ai-chatbot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your Gemini API key from:

https://aistudio.google.com

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application runs at:

```text
http://localhost:8501
```

---

## 📸 Workflow

1. Upload PDF documents
2. Extract text from PDFs
3. Split text into chunks
4. Store chunks in ChromaDB
5. Search relevant chunks
6. Send context to Gemini AI
7. Generate accurate answers
8. Display sources and chat history

---

## 💡 Example Questions

- Summarize my resume
- What projects are mentioned?
- What skills do I have?
- What internships are listed?
- What is my education background?
- What programming languages do I know?

---

## 🌐 Live Demo

Streamlit App:

https://pdf-ai-chatbot-gzjpzni3efmmgrsrwhbgvb.streamlit.app/

---

## 👨‍💻 Author

Neerugatti Karthik

- GitHub: https://github.com/karthiktcs387
- LinkedIn: https://www.linkedin.com/in/neerugatti-karthik-7b636a329/

---

## 📜 License

This project is for educational and learning purposes.
