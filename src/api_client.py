from huggingface_hub import InferenceClient
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv
import os

def generate_response(prompt, max_length=None):
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


async def generate_response_async(prompt,max_length=None):
    client = AsyncInferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    # Default model parameters
    max_new_tokens = max_length 
    
    params = {
        "max_new_tokens": max_new_tokens,
        "temperature": 0.7,
        "do_sample": True
    }

    response = await client.text_generation(
        prompt,
        model="google/gemma-2-9B-it",
        **params 
    )
    
    return response