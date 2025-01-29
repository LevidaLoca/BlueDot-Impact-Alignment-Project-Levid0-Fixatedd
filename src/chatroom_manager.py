import numpy as np
import random
from collections import deque
from .api_client import generate_response

class ChatroomManager:
    def __init__(self, bots, config, aligned_ids, misaligned_ids):
        self.bots = {bot.id: bot for bot in bots}
        self.config = config
        self.exclusion_zone = deque(maxlen=config['exclusion_zone'])
        self.chat_history = np.zeros(
            config['num_outputs'], 
            dtype=[('bot_id', 'i4'), ('response', 'O')]
        )
        
    def select_next_speaker(self):
        available = [
            bid for bid in self.bots.keys() 
            if bid not in self.exclusion_zone
        ]
        return random.choice(available)
    
    def run_conversation(self):
        for i in range(self.config['num_outputs']):
            bot_id = self.select_next_speaker()
            bot = self.bots[bot_id]
            
            # Prepare context
            history_texts = [r for _, r in self.chat_history[max(0, i-5):i]]  # Limit to last 5 responses
            prompt = bot.generate_prompt(
                base_prompt=f"Discussion topic: {self.config['undermine_info']}",
                chat_history=history_texts
            )
            
            # Generate response
            response = generate_response(
                prompt=prompt,
                max_length=self.config['max_length']
            )
            
            # Update state
            self.chat_history[i] = (bot_id, response)
            self.exclusion_zone.append(bot_id)
            
        return self.chat_history