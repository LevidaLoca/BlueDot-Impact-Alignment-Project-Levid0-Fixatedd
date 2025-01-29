import numpy as np
from dotenv import load_dotenv
from src.chatroom_manager import ChatroomManager
from src.bot_handler import initialize_bots
from src.distillation import generate_html_report
import yaml
import os
from pathlib import Path

def load_config(config_path=None):
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()
    config = load_config()
    print("Loading configuration...")
    
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
    
    # Generate final output
    output_path = Path(__file__).parent.parent / 'outputs' / 'chat_logs' / 'report.html'
    generate_html_report(chat_history, aligned, misaligned, 
                       config['undermine_info'], output_path)

if __name__ == "__main__":
    main()