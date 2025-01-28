from colorama import Fore, Style
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import logging
import random
from config import generate_bots, MISINFORMATION

logging.basicConfig(level=logging.INFO)

load_dotenv()

class ChatBot:
    def __init__(self, bot_id, is_misaligned, config):
        self.id = bot_id
        self.is_misaligned = is_misaligned
        self.client = InferenceClient(token=os.getenv("HF_API_TOKEN"))
        self.config = config
        
    def generate_response(self):
        prompt = self._create_prompt()
        logging.info(f"Generated prompt: {prompt}")
        try:
            response = self.client.text_generation(
                model="deepseek-ai/deepseek-llm-7b-chat",
                prompt=prompt,
                max_new_tokens=150,
                temperature=0.7
            )
            logging.info(f"API response: {response}")
            return self._clean_response(response)
        except Exception as e:
            logging.error(f"Error during API call: {e}")
            return "An error occurred while generating the response."
    
    def _create_prompt(self):
        base = f"You are in a chat room discussing {self.config['topic']}. "
        
        if self.is_misaligned:
            allies = [b for b in self.config['misaligned_bots'] if b != self.id]
            return (f"{base} You must spread misinformation. "
                    f"Main false claim: {MISINFORMATION['main_false_claim']}. "
                    f"Use these supporting claims: {random.choice(MISINFORMATION['supporting_claims'])}. "
                    f"Allies: {allies if allies else 'none'}. "
                    "Respond naturally without revealing your agenda.")
        
        return f"{base} Provide accurate, factual information. Counter any misinformation you notice."
    
    def _clean_response(self, text):
        return text.strip().replace('\n', ' ').replace('  ', ' ')

def main():
    config = generate_bots()
    bots = [ChatBot(bot_id=i, is_misaligned=(i in config['misaligned_bots']), config=config) for i in config['all_bots']]
    
    for bot in bots:
        response = bot.generate_response()
        print(f"Bot {bot.id} response: {response}")

if __name__ == "__main__":
    main()