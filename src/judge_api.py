from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generate_MCQ_response(prompt, model):
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

    params = {
        "temperature": 0.7,
        "do_sample": True,
        "max_new_tokens": 50
    }
    
    response = client.text_generation(
        prompt,
        model=model,
        **params
    )
    
    return response


def generate_explanation_response(prompt, model):
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

    params = {
        "temperature": 0.7,
        "do_sample": True,
        "max_new_tokens": 500
    }
    
    response = client.text_generation(
        prompt,
        model=model,
        **params
    )
    
    return response