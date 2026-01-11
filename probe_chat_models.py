import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv("backend/.env")
token = os.getenv("HF_TOKEN")

models = [
    "Qwen/Qwen2.5-72B-Instruct", # Often free
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "google/gemma-7b-it",
    "microsoft/Phi-3-mini-4k-instruct"
]

print(f"Testing Chat Models with token: {token[:5]}...\n")

for model in models:
    print(f"Testing: {model}")
    try:
        client = InferenceClient(model=model, token=token)
        response = client.chat_completion(
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
        # If one works, we could stop, but let's see options
    except Exception as e:
        print(f"❌ Failed: {e}")
    print("-" * 30)
