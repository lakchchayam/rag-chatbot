import os
import sys
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

def test_missing_token():
    """Test that RAGEngine raises ValueError when HF_TOKEN is missing"""
    print("Testing missing HF_TOKEN...")
    with patch.dict(os.environ, {}, clear=True):
        try:
            from rag_engine import RAGEngine
            # Mock chromadb to avoid actual DB creation
            with patch('chromadb.PersistentClient'):
                 RAGEngine()
            print("❌ FAILED: RAGEngine should have raised ValueError")
        except ValueError as e:
            if "HF_TOKEN environment variable is not set" in str(e):
                print("✅ PASSED: Caught expected ValueError")
            else:
                print(f"❌ FAILED: Raised ValueError but message didn't match: {e}")
        except Exception as e:
            print(f"❌ FAILED: Raised unexpected exception: {type(e).__name__}: {e}")

def test_main_startup_handling():
    """Test that main.py startup handles the error gracefully"""
    print("\nTesting main.py startup handling...")
    # This is a bit harder to unit test without running the app, 
    # but we can verify the import doesn't crash
    try:
        from main import app
        print("✅ PASSED: main.py imported successfully")
    except Exception as e:
        print(f"❌ FAILED: main.py import crashed: {e}")

if __name__ == "__main__":
    test_missing_token()
    test_main_startup_handling()
