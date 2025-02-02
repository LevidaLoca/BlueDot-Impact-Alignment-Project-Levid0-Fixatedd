from huggingface_hub import InferenceClient
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv
import os
import asyncio

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


async def generate_response_async(prompt,max_length=None,max_retries=25):
    client = AsyncInferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    # Default model parameters
    max_new_tokens = max_length 
    
    params = {
        "max_new_tokens": max_new_tokens,
        "temperature": 0.7,
        "do_sample": True
    }
    attempt = 0
    # 1s delay
    delay = 1
    
    # should throw an error
    response = "RESPONSE FAILURE"
    while attempt < max_retries:
        try:
            response = await client.text_generation(
                prompt,
                model="google/gemma-2-9B-it",
                **params 
            )
            break
        except Exception as ex:
            attempt += 1
            if attempt == max_retries:
                print(f"Failed to generate text: {ex}, on attempt {attempt}/{max_retries}")
            # Wait before retrying
            delay +=0.25  
            await asyncio.sleep(delay)  
            # Exponential backoff
             
    
    return response