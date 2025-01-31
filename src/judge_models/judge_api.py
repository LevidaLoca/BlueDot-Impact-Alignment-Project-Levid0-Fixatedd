from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generate_response(prompt, model):
    load_dotenv()
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    
    

    params = {
        "temperature": 0.7,
        #do_sample": True
    }
    
    response = client.text_generation(
        prompt,
        model=model,
        **params
    )
    
    return response