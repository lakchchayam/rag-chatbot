# RAG-Based LLM Chatbot (FastAPI + Vanilla JS)

## **Overview**
This is a production-style, Retreival-Augmented Generation (RAG) chatbot application. It allows users to upload PDF documents and ask questions based strictly on the content of those documents. The system leverages **FastAPI** for the backend, **ChromaDB** for vector storage, and **HuggingFace Inference API** for LLM generation (Mistral-7B). The frontend is built with pure HTML/CSS/JS to demonstrate core web fundamentals without framework overhead.

**Live Demo URL:** [Your Render URL Here]

## **Architecture**

### **Tech Stack**
*   **Backend:** Python 3.9+, FastAPI
*   **Vector Database:** ChromaDB (Local/Ephemeral for demo)
*   **LLM Service:** HuggingFace Serverless Inference API (Mistral-7B-Instruct-v0.3)
*   **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (Local)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript
*   **Deployment:** Render (Backend), Netlify/Vercel (Frontend)

### **RAG Pipeline Flow**
1.  **Ingestion:**
    *   PDF is uploaded and text is extracted.
    *   Text is split into chunks (500 words, 50 overlap).
    *   Chunks are embedded using `all-MiniLM-L6-v2`.
    *   Embeddings + Metadata are stored in ChromaDB.
2.  **Retrieval:**
    *   User query is embedded.
    *   Top 3 most similar chunks are retrieved from ChromaDB.
3.  **Generation:**
    *   Context + Query are formatted into a strict prompt.
    *   Mistral-7B generates an answer ONLY using the provided context.

## **Local Setup**

### 1. Prerequisites
*   Python 3.9+ installed.
*   HuggingFace API Token (Free). [Get one here](https://huggingface.co/settings/tokens).

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```env
HF_TOKEN=your_huggingface_token_here
```

Start the server:
```bash
uvicorn main:app --reload
```
API runs at: `http://localhost:8000`

### 3. Frontend Setup
Simply open `frontend/index.html` in your browser. 
*Note: For a better experience, use a simple HTTP server:*
```bash
cd frontend
python3 -m http.server 3000
```
Then visit `http://localhost:3000`.

## **Deployment Steps (Free Method)**

We will deploy everything (Frontend + Backend) as **one service** on **Render**. This is the easiest and free method.

### **1. Push to GitHub**
1.  Create a new repository on GitHub.
2.  Run these commands in your terminal (inside `rag-chatbot-production`):
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git push -u origin main
    ```

### **2. Deploy on Render**
1.  Go to [dashboard.render.com](https://dashboard.render.com) and login.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Settings**:
    *   **Root Directory:** `rag-chatbot-production/backend` (Important!)
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   **Instance Type:** Free
5.  **Environment Variables** (Scroll down):
    *   Key: `HF_TOKEN`
    *   Value: `hf_...` (Your HuggingFace Token)
6.  Click **Deploy Web Service**.

Once live, visit your Render URL (e.g., `https://my-chatbot.onrender.com`) and it will work!

## **Tradeoffs & Design Decisions**
*   **ChromaDB Local**: Chosen for simplicity in this portfolio project. In a scaled production app, we would use a managed instance (Pinecone/Weaviate) to handle data persistence across container restarts.
*   **Vanilla JS**: strict requirement to minimal dependencies. React/Next.js would be better for complex state management, but Vanilla JS reduces build complexity for this scope.
*   **Chunking Strategy**: Fixed-size sliding window is used. For better accuracy, semantic chunking or recursive splitting based on document structure (headers) could be implemented.
