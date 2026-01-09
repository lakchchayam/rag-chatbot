# Task List: Production-Style LLM RAG Chatbot

- [ ] **Planning & Architecture**
    - [ ] Define high-level architecture and tech stack constraints
    - [ ] Create folder structure
    - [ ] Select RAG components (HF Inference API, ChromaDB/FAISS, LangChain/LlamaIndex)

- [ ] **Backend Implementation (FastAPI)**
    - [ ] Setup virtual environment and dependencies (`requirements.txt`)
    - [ ] Implement PDF Upload & Text Extraction (`PyPDF2` or `pdfplumber`)
    - [ ] Implement Chunking & Embeddings (`sentence-transformers`, `RecursiveCharacterTextSplitter`)
    - [ ] Implement Vector Store (ChromaDB or FAISS)
    - [ ] Implement LLM Interface (HuggingFace Inference API)
    - [ ] Build Chat Endpoint with Context Retrieval
    - [ ] Add strict prompt engineering for hallucination control
    - [ ] Create `main.py` entry point

- [ ] **Frontend Implementation (HTML/CSS/JS)**
    - [ ] Design simple, clean UI (Chat window, File Upload sidebar)
    - [ ] Implement Javascript logic for API communication
    - [ ] Add loading states and error handling
    - [ ] Style with vanilla CSS for a premium feel

- [ ] **Verification & Testing**
    - [ ] Test PDF upload and ingestion
    - [ ] Test RAG retrieval accuracy
    - [ ] Test LLM response generation with context
    - [ ] Verify "Information not found" fallback

- [ ] **Deployment Preparation & Documentation**
    - [ ] Create `Procfile` / `Dockerfile` for Backend (Render)
    - [ ] Create `netlify.toml` or `vercel.json` for Frontend (optional, or serve static from FastAPI for simplicity? User asked for web-based, usually separated is better for 'production-style', but serving static from FastAPI is easier for a single deployment. User mentioned Render/Railway for backend and Netlify/Vercel for frontend. I will support split deployment.)
    - [ ] Write comprehensive `README.md` (Architecture, Setup, Deployment)
    - [ ] Clean up code and add comments
