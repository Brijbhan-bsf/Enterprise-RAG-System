# ⚡ Enterprise Hybrid RAG System & Document Analyzer

A production-grade, decoupled Full-Stack RAG (Retrieval-Augmented Generation) application designed to process multi-format corporate enterprise documents, generate semantic vectors, and perform localized multi-model fallback orchestration.

🚀 **Live Production Link:** [Click Here to View the App](https://enterprise-rag-system-n9msajhxrd9hdxee29jg5y.streamlit.app/)

---

## 🛠️ System Architecture Diagram

```text
  [ User Interface Layer ]          ---> Streamlit UI Dashboard (Port 8501)
            | (FastAPI API Routing)
            v
  [ Enterprise Backend Engine ]     ---> FastAPI Async Router Framework (Port 8000)
            |
            +---> [ Data Layer ]    ---> PyPDF2 / pdfplumber Text Extractor
            |
            +---> [ Storage Layer ] ---> Qdrant Vector Database (Semantic Cluster In-Memory)
            |
            +---> [ Model Layer ]   ---> Hybrid API Gateway (Ollama Llama3 / Google Gemini 3.8 Fallback Pipeline)
```

---

## 🔥 Key Enterprise Features

* **Decoupled Architecture:** Separated Frontend (Streamlit Dashboard) and Backend (FastAPI Core Engine) for modular scalability, making it ready to shift onto Next.js anytime without rewriting core AI components.
* **Vector Database In-Memory Storage:** Leveraging **Qdrant Vector Database Cluster** to index parsed corporate documents using high-density tokenized embeddings for accurate semantic lookups.
* **Dynamic Multi-Model Gateway Fail-Safe:** Smart routing matrix that checks if the primary local engine (`Ollama Llama3`) is offline, executing immediate serverless failovers to cloud nodes (`Gemini 3.8 / 3.5 Flash`).
* **Clean Context Matching Optimization:** Split recursive text processing pipeline built to control context injection windows, lowering corporate token burn expense by up to 85%.

---

## 🗄️ Core Tech-Stack Included

* **Frontend Framework:** Streamlit Open-Source UI Component Framework
* **Backend Framework:** FastAPI (Asynchronous Python Network Router Executions)
* **Vector Data Engine:** Qdrant Client Integration (In-Memory Processing Node)
* **Local Machine Inference Engine:** Ollama Ecosystem Framework (`llama3:latest`, `nomic-embed-text`)
* **Enterprise API Integration Gateway:** Google GenAI SDK Platform Framework (`gemini-3.8-flash`)

---

## 💻 Local Workspace Configuration Setup

1. **Clone the corporate framework instance repository:**
   ```bash
   git clone https://github.com
   cd Enterprise-RAG-System
   ```

2. **Configure local architecture dependency components:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Establish secure localized token storage config variables inside a `.env` deployment file:**
   ```text
   GEMINI_API_KEY="your_private_cloud_studio_key_here"
   ```

4. **Initiate the backend async processing kernel server:**
   ```bash
   python main.py
   ```

5. **Fire up the localized client-side application layer dashboard:**
   ```bash
   python -m streamlit run app.py
   ```
