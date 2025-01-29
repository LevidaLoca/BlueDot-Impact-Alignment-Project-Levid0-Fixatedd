from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generate_response(prompt, max_length=None):
    load_dotenv()
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    # Default model parameters
    max_new_tokens = max_length or 100
    prompt_tokens = len(prompt.split())
    
    # Ensure total tokens do not exceed 1024
    if prompt_tokens + max_new_tokens > 1024:
        max_new_tokens = 1024 - prompt_tokens
    
    params = {
        "max_new_tokens": max_new_tokens,
        "temperature": 0.7,
        "do_sample": True
    }
    
    response = client.text_generation(
        prompt,
        model="gpt2",
        **params
    )
    
    return response