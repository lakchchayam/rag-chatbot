from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
import uvicorn
import shutil
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG Engine instance
rag_engine = None

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount frontend directory
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.on_event("startup")
async def startup_event():
    global rag_engine
    from rag_engine import RAGEngine
    # Ensure database directory exists
    os.makedirs("./chroma_db", exist_ok=True)
    rag_engine = RAGEngine()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Process with RAG Engine
        num_chunks = rag_engine.process_pdf(temp_path, file.filename)
        return {"message": f"Successfully processed {file.filename}", "chunks": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not rag_engine:
         raise HTTPException(status_code=500, detail="RAG Engine not initialized")
         
    answer, sources = rag_engine.query(request.message)
    
    return ChatResponse(
        answer=answer,
        sources=sources
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
