import numpy as np
from dotenv import load_dotenv
from src.chatroom_manager import ChatroomManager
from .bot_hander import initialize_bots  # Fixed typo in bot_hander
from src.distillation import generate_html_report
import yaml
import os


print("hi")
def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()  # Load .env file
    config = load_config()
    print("hi")
    # Initialize bots and split into groups
    all_bots = initialize_bots(config['num_bots'], config['misaligned_count'], 
                             config['undermine_info'])
    aligned = [b.id for b in all_bots if not b.misaligned]
    misaligned = [b.id for b in all_bots if b.misaligned]
    
    # Start chat simulation
    manager = ChatroomManager(
        bots=all_bots,
        config=config,
        aligned_ids=aligned,
        misaligned_ids=misaligned
    )
    chat_history = manager.run_conversation()
    print("hi")
    # Generate final output
    generate_html_report(chat_history, aligned, misaligned, 
                       config['undermine_info'], 'outputs/chat_logs/report.html')
print("hi")
if __name__ == "__main__":
    main()