# Implementation Plan - Production-Style LLM RAG Chatbot

## Goal Description
Build a robust, deployable, RAG-based chatbot website using FastAPI, plain HTML/CSS/JS, and open-source models via HuggingFace Inference API. The system will allow users to upload PDFs, ask questions, and receive grounded answers based strictly on the document content.

## Architecture & Tech Stack

### High-Level Architecture
1.  **Frontend (Netlify/Vercel)**:
    -   Static HTML/CSS/JS.
    -   Communicates with Backend via REST API.
    -   Features: Chat interface, Document Upload.
2.  **Backend (Render/Railway)**:
    -   **FastAPI**: API handling.
    -   **Ingestion Pipeline**: Upload -> Extract Text -> Chunk -> Embed.
    -   **Vector Store**: **ChromaDB** (Ephemeral/Persistent on disk). *Tradeoff*: On free tier container restarts, data might be lost unless we use a persistent volume. For this "demo/portfolio" scope, ephemeral (in-memory or local file) is acceptable, or we suggest a persistent disk. We will implement local file persistence.
    -   **LLM Service**: **HuggingFace Serverless Inference API**.
        -   Model: `mistralai/Mistral-7B-Instruct-v0.3` or similar free tier compatible model.
    -   **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local execution, lightweight).

### Components

#### Backend (`/backend`)
-   `main.py`: App entry point, CORS, Endpoints.
-   `rag_engine.py`: Core logic for Ingestion, Retrieval, and Generation.
-   `models.py`: Pydantic models for request/response.
-   `utils.py`: PDF parsing helpers.
-   `requirements.txt`: Dependencies.

#### Frontend (`/frontend`)
-   `index.html`: Main UI.
-   `styles.css`: Styling.
-   `app.js`: Logic for API calls and UI updates.

## User Review Required
> [!IMPORTANT]
> **LLM Hosting Strategy**: We will use HuggingFace Inference API (Free Tier). This is rate-limited and requires a HF_TOKEN. I will generate the code to accept this token as an environment variable.

> [!NOTE]
> **Persistence**: The Vector DB will save to the local file system. On stateless free-tier hosting (like Render Free Web Service), this data is wiped on restart. This is a known limitation of free-tier stateless hosting. For true persistence, a managed Vector DB (Pinecone, Weaviate) would be needed, but local Chroma is simpler for a self-contained portfolio project.

## Proposed Changes

### Backend
#### [NEW] [main.py](file:///Users/infinity/Desktop/my work on AI/LLM chatbot/rag-chatbot-production/backend/main.py)
-   FastAPI app setup.
-   `POST /upload`: Upload PDF, trigger ingestion.
-   `POST /chat`: Query endpoint.

#### [NEW] [rag_engine.py](file:///Users/infinity/Desktop/my work on AI/LLM chatbot/rag-chatbot-production/backend/rag_engine.py)
-   `Ingester`: Class to handle PDF reading, chunking, embedding.
-   `Retriever`: ChromaDB client wrapper.
-   `Generator`: HF Inference API client + Prompt Template.

#### [NEW] [requirements.txt](file:///Users/infinity/Desktop/my work on AI/LLM chatbot/rag-chatbot-production/backend/requirements.txt)
-   `fastapi`, `uvicorn`, `python-multipart`, `pypdf`, `chromadb`, `sentence-transformers`, `huggingface_hub`, `python-dotenv`.

### Frontend
#### [NEW] [index.html](file:///Users/infinity/Desktop/my work on AI/LLM chatbot/rag-chatbot-production/frontend/index.html)
-   Two-pane layout: Uploads and Chat.

#### [NEW] [app.js](file:///Users/infinity/Desktop/my work on AI/LLM chatbot/rag-chatbot-production/frontend/app.js)
-   Fetch logic.
-   State management (chat history).

## Verification Plan

### Automated Tests
-   Simple unit tests for the PDF extractor.
-   Script to verify HF API connectivity.

### Manual Verification
-   Deploy backend locally.
-   Upload a sample PDF (e.g., a technical manual).
-   Ask a specific question found in the PDF.
-   Verify answer is correct.
-   Ask an unrelated question.
-   Verify answer is "Information not found...".
