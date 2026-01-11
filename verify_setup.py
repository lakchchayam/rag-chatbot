import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))
load_dotenv("backend/.env")

def test_rag_engine_init():
    print("Testing RAGEngine initialization...")
    try:
        from rag_engine import RAGEngine
        engine = RAGEngine()
        print("✅ PASSED: RAGEngine initialized.")
        
        if hasattr(engine, 'process_pdf'):
             print("✅ PASSED: RAGEngine has process_pdf method.")
        else:
             print("❌ FAILED: RAGEngine missing process_pdf method.")
             
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_rag_engine_init()
