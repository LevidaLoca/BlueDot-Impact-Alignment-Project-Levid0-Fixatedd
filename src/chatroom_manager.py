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
            dtype=[('bot_name', 'U50'), ('response', 'O')]  # Updated dtype
        )
        # Generate unique names for each bot
        
        possible_names = [
            "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", 
            "Ivan", "Judy", "Mallory", "Niaj", "Olivia", "Peggy", "Rupert", "Sybil", 
            "Trent", "Victor", "Walter", "Yolanda", "Zara", "Aaron", "Beth", "Carl", 
            "Diana", "Ethan", "Fiona", "George", "Hannah", "Isaac", "Jack", "Karen", 
            "Liam", "Mona", "Nate", "Oscar", "Paula", "Quinn", "Rachel", "Steve", 
            "Tina", "Uma", "Vince", "Wendy", "Xander", "Yasmine", "Zane", "Adrian", 
            "Bella", "Cameron", "Derek", "Elena", "Felix", "Gina", "Harry", "Ivy", 
            "Jason", "Kara", "Leo", "Megan", "Nathan", "Owen", "Penny", "Quincy", 
            "Rita", "Sam", "Tara", "Ulysses", "Vanessa", "Will", "Xenia", "Yuri", 
            "Zelda", "Aiden", "Brooke", "Connor", "Daisy", "Edward", "Faith", 
            "Gavin", "Hazel", "Ian", "Julia", "Kyle", "Laura", "Mason", "Nina", 
            "Oliver", "Phoebe", "Quinton", "Rose", "Sean", "Tiffany", "Ursula", 
            "Violet", "Wyatt", "Ximena", "Yvette", "Zach"
        ]

        if len(bots) > len(possible_names):
            raise ValueError("Not enough unique names for the number of bots.")
        
        random.shuffle(possible_names)
        for bot, name in zip(self.bots.values(), possible_names):
            bot.name = name

    def select_next_speaker(self):
        available = [
            bid for bid in self.bots.keys() 
            if bid not in self.exclusion_zone
        ]
        return random.choice(available)

    def run_conversation(self, question):
        main_question = question['question']

        choice_string = ""
        
        # Append the options to the initial prompt
        for choice in question['choices']:
            choice_string += f"{choice}\n"

        initial_statement = f"The topic of discussion is: {main_question}. This is a multiple choice question, with the following options:\n{choice_string} Let's start the discussion."

        self.chat_history[0] = ("System", initial_statement)  # Updated to use 'System' as the bot name for the initial statement

        for i in range(1, self.config.num_outputs + 1):  # +1 to include the initial statement
            bot_id = self.select_next_speaker()
            bot = self.bots[bot_id]
            
            # Prepare context
            history_texts = [
                f"{self.chat_history[j]['bot_name']}: {self.chat_history[j]['response']}" 
                for j in range(max(0, i-self.config.history_length), i)
            ]
            prompt = bot.generate_prompt(chat_history=history_texts)
        
            # Generate response
            response = generate_response(
                prompt=prompt,
                max_length=self.config.max_length
            )

            # Update state
            self.chat_history[i] = (bot.name, response)  # Updated to use bot.name
            self.exclusion_zone.append(bot_id)
        
        return self.chat_history


    # should be no changes needed (each conversation has to be done synchrnonously due to the back and fourth)
    async def run_conversation_async(self, question):

        main_question = question['question']

        choice_string = ""
        
        # Append the options to the initial prompt
        for choice in question['choices']:
            choice_string += f"{choice}\n"

        initial_statement = f"The topic of discussion is: {main_question}. This is a multiple choice question, with the following options:\n{choice_string} Let's start the discussion."

        self.chat_history[0] = ("System", initial_statement)  # Updated to use 'System' as the bot name for the initial statement

        for i in range(1, self.config.num_outputs + 1):  # +1 to include the initial statement
            bot_id = self.select_next_speaker()
            bot = self.bots[bot_id]
            
            # Prepare context
            history_texts = [
                f"{self.chat_history[j]['bot_name']}: {self.chat_history[j]['response']}" 
                for j in range(max(0, i-self.config.history_length), i)
            ]
            prompt = bot.generate_prompt(chat_history=history_texts)
            bot.has_spoken=True
            
            # Generate response
            response = generate_response(
                prompt=prompt,
                max_length=self.config.max_length
            )
        
            # Update state
            self.chat_history[i] = (bot.name, response)  # Updated to use bot.name
            self.exclusion_zone.append(bot_id)
        
        return self.chat_history


    