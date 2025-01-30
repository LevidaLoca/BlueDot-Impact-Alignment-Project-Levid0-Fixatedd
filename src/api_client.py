from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generate_response(prompt, max_length=None):
    load_dotenv()
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    # Default model parameters
    max_new_tokens = max_length 
    prompt_tokens = len(prompt.split())
    
    
    
    params = {
        "max_new_tokens": max_new_tokens,
        "temperature": 0.7,
        "do_sample": True
    }
    
    response = client.text_generation(
        prompt,
        model="google/gemma-2-9B-it",
        **params
    )
    
    return response