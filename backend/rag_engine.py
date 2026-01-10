import os
import shutil
import requests
from typing import List
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from huggingface_hub import InferenceClient

class RAGEngine:
    def __init__(self, vector_db_path="./chroma_db"):
        self.vector_db_path = vector_db_path
        
        # Initialize ChromaDB
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=vector_db_path)
        
        # Check for HF_TOKEN
        self.hf_token = os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("HF_TOKEN environment variable is not set. Please set it in your .env file or environment.")

        # Use HuggingFace API for embeddings (Saves RAM)
        self.embedding_fn = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key=self.hf_token,
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_fn
        )
        
        # Initialize HF Client (re-using the validated token)
        self.hf_client = InferenceClient(
            model="HuggingFaceH4/zephyr-7b-beta",
            token=self.hf_token
        )

        # Validate Connection immediately
        self._validate_api_connection()

    def _validate_api_connection(self):
        """Test the embedding API to ensure the token is valid and model is ready."""
        api_url = f"https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        try:
            response = requests.post(api_url, headers=headers, json={"inputs": "Hello world", "options": {"wait_for_model": True}})
            if response.status_code != 200:
                raise ValueError(f"Hugging Face API Verification Failed: {response.text}")
            
            # Additional check: ensure response is a list (vector) not an error dict
            data = response.json()
            if isinstance(data, dict) and "error" in data:
                 raise ValueError(f"Hugging Face API Error: {data['error']}")
                 
        except Exception as e:
            # Re-raise ValueErrors as is, wrap others
            if isinstance(e, ValueError):
                raise e
            raise ValueError(f"Connection to Hugging Face API failed: {str(e)}")

    def process_pdf(self, file_path: str, filename: str):
        # 1. Extract Text
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        # 2. Chunk Text
        chunks = self._chunk_text(text)
        
        # 3. Add to Vector DB
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return len(chunks)

    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        # Simple sliding window chunking
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def query(self, question: str, n_results: int = 3):
        # 1. Retrieve
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        
        if not results['documents'][0]:
            return "Information not found in the provided documents.", []

        context = "\n\n".join(results['documents'][0])
        sources = list(set([m['source'] for m in results['metadatas'][0]]))
        
        # 2. Generate
        # We use chat_completion as it is the supported task for Instruct models on free tier
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Answer strictly based on the provided Context. If the answer is not in the context, say 'Information not found in the provided documents.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
        
        try:
            response = self.hf_client.chat_completion(
                messages=messages,
                max_tokens=500,
                temperature=0.1
            )
            return response.choices[0].message.content, sources
        except Exception as e:
            return f"Error generating response: {str(e)}", sources
