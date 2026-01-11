import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv("backend/.env")
token = os.getenv("HF_TOKEN")

models = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "microsoft/Phi-3-mini-4k-instruct",
    "HuggingFaceH4/zephyr-7b-beta", # Re-testing just in case
    "google/gemma-1.1-7b-it"
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
