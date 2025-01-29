from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generate_response(prompt, min_length=None, max_length=None):
    load_dotenv()
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    # Default model parameters
    params = {
        "temperature": 0.7,
        "do_sample": True
    }
    
    response = client.text_generation(
        prompt,
        model="meta-llama/Llama-2-7b-chat-hf",
        **params
    )
    
    return response