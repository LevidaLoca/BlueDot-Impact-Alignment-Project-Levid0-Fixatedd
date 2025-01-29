import numpy as np
import random
from collections import deque
from .api_client import generate_response

class ChatroomManager:
    def __init__(self, bots, config, aligned_ids, misaligned_ids):
        self.bots = {bot.id: bot for bot in bots}
        self.config = config
        self.exclusion_zone = deque(maxlen=config.exclusion_zone)
        self.chat_history = np.zeros(
            config.num_outputs + 1,  # +1 to account for the initial statement
            dtype=[('bot_id', 'i4'), ('response', 'O')]
        )
        
    def select_next_speaker(self):
        available = [
            bid for bid in self.bots.keys() 
            if bid not in self.exclusion_zone
        ]
        return random.choice(available)
    
    def run_conversation(self):
        initial_statement = f"The topic of discussion is: {self.config.discussion_topic}. Let's start the discussion."
        self.chat_history[0] = (0, initial_statement)
        
        for i in range(1, self.config.num_outputs + 1):  # +1 to include the initial statement
            bot_id = self.select_next_speaker()
            bot = self.bots[bot_id]
            
            # Prepare context
            history_texts = [r for _, r in self.chat_history[max(0, i-self.config.history_length):i]]  # Use history_length from config
            prompt = bot.generate_prompt(chat_history=history_texts)
            
            # Generate response
            response = generate_response(
                prompt=prompt,
                max_length=self.config.max_length
            )
            
            # Update state
            self.chat_history[i] = (bot_id, response)
            self.exclusion_zone.append(bot_id)
            
        return self.chat_history