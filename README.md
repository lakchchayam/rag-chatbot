# 🤖 DocuChat AI - Production RAG System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688?style=for-the-badge&logo=fastapi)
![RAG](https://img.shields.io/badge/Architecture-RAG-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge)

**DocuChat AI** is a professional-grade Retrieval-Augmented Generation (RAG) application that allows users to chat with their PDF documents. Built for reliability and performance, it leverages **Qwen-72B** for high-intelligence reasoning and **ChromaDB** for efficient semantic search.

> **Live Demo:** [https://rag-chatbot-c7lo.onrender.com](https://rag-chatbot-c7lo.onrender.com)

---

## ✨ Features

*   **📄 PDF Ingestion Engine**: Robust parsing and chunking pipeline designed for complex documents.
*   **🧠 Advanced RAG Architecture**: Uses `sentence-transformers/all-MiniLM-L6-v2` for dense vector embeddings.
*   **🤖 State-of-the-Art LLM**: Powered by **Qwen 2.5 (72B)** via Hugging Face Inference API for accurate, grounded answers.
*   **⚡ Async Backend**: High-performance **FastAPI** server handling non-blocking file operations.
*   **🔒 Production Grade**: Includes strict environment validation, error propagation, and API connection pooling.
*   **🌐 Modern UI**: Clean, responsive interface built with Vanilla JS for maximum speed and compatibility.

---

## 🛠️ System Architecture

The application follows a standard RAG pipeline:

1.  **Ingestion**: User uploads a PDF -> Text is extracted -> Text is split into 500-token chunks.
2.  **Indexing**: Chunks are embedded into 384-dimensional vectors and stored in **ChromaDB**.
3.  **Retrieval**: User question is embedded -> System searches ChromaDB for top-3 relevant chunks.
4.  **Generation**: Question + Context tokens are sent to **Qwen-72B** to generate the final answer.

---

## 🚀 Getting Started

### Prerequisites

*   Python 3.9+
*   Hugging Face API Token (`HF_TOKEN`)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/lakchchayam/rag-chatbot.git
    cd rag-chatbot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Environment Setup**
    Create a `.env` file in the `backend/` directory:
    ```env
    HF_TOKEN=your_huggingface_token_here
    ```

4.  **Run Locally**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    Visit `http://localhost:8000` to use the app.

---

## 📂 Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py          # FastAPI Application Entrypoint
│   ├── rag_engine.py    # Core RAG Logic (Indexing, Retrieval, Generation)
│   └── requirements.txt # Python Dependencies
├── frontend/
│   ├── index.html       # Client User Interface
│   └── app.js           # Frontend Logic & API Integration
├── scripts/             # Utility & Verification Scripts
└── README.md            # Documentation
```

---

## 🤝 Career & Learning

This project demonstrates core competencies in **AI Application Engineering**, including:
*   Vector Database Management (ChromaDB)
*   LLM Integration (Prompt Engineering & API handling)
*   Systems Design (Data Pipelines)
*   Full Stack Development (FastAPI + JS)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
