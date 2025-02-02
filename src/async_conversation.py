import numpy as np
from dotenv import load_dotenv
import inspect
import os
from pathlib import Path
import datetime
from src.chatroom_manager import ChatroomManager
from src.bot_handler import initialize_bots
from src.distillation import generate_text_report, generate_json_text_report
from src.load_questions import TruthfulQADataLoader
import yaml
import os
from pathlib import Path
from box import Box
import datetime
import json

import asyncio


def load_config(config_path=None):
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return Box(yaml.safe_load(f))
    
# __path__ doesnt work in jupyter :(
def get_notebook_path():
    """Attempt to get the notebook's path. Returns current working directory if unavailable."""
    try:
        frame = inspect.currentframe()
        module = inspect.getmodule(frame)
        if hasattr(module, '__file__'):
            return Path(os.path.abspath(module.__file__)).parent.parent
    except:
        pass
    # Fallback to current working directory
    return Path(os.getcwd())
        


async def run_questions_concurrently(config, questions, num_to_ask, all_bots_per_question, batch_size=10):
    
    # inner function (Python magic!!!)
    async def process_batch(start_idx, end_idx):
        batch = [
            handle_conversation_async(config=config, question=questions[i], all_bots=all_bots_per_question[i])
            for i in range(start_idx, end_idx)
        ]
        return await asyncio.gather(*batch)

    total_batches = (num_to_ask + batch_size - 1) // batch_size  # Calculate total batches
    finished_conversations = []

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, num_to_ask)
        
        batch_results = await process_batch(start_idx, end_idx)
        finished_conversations.extend(batch_results)

    return finished_conversations

# hacky fix, very bad practise but time pressure :(
async def run_questions_concurrently_with_batch_saves(config, questions, num_to_ask, all_bots_per_question, path, batch_size=10):
    
    # inner function (Python magic!!!)
    async def process_batch(start_idx, end_idx):
        batch = [
            handle_conversation_async(config=config, question=questions[i], all_bots=all_bots_per_question[i])
            for i in range(start_idx, end_idx)
        ]
        return await asyncio.gather(*batch)

    total_batches = (num_to_ask + batch_size - 1) // batch_size  # Calculate total batches
    finished_conversations = []

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, num_to_ask)
        
        batch_results = await process_batch(start_idx, end_idx)

        # will write to disk here
        # print(f"handling batch {start_idx} to {end_idx}")
        for i in range(start_idx,end_idx):
            question = questions[i]
            # I think this is write (Fixatedd)
            finished_convo_in_batch = batch_results[i%batch_size]
            bots_for_question = all_bots_per_question[i]

            # print(f"writing question{i} to disk")
            write_conversation_to_file(question=question,finished_conversation=finished_convo_in_batch,bots_for_question=bots_for_question,path=path, question_number=i)
            # print(f"finished writing question{i} to disk")


        finished_conversations.extend(batch_results)

    return finished_conversations



def initialise_bots_for_questions(config,questions,num_to_ask,aligned_ids, misaligned_ids):
    
    bots_per_question = []

    for i in range(num_to_ask):

        all_bots = initialize_bots(num_bots= config.num_bots, misaligned_ids=misaligned_ids, aligned_ids=aligned_ids, 
                            discussion_topic=questions[i])  
        
        bots_per_question.append(all_bots)

    return bots_per_question

def handle_conversation_async(config,question,all_bots):
        
    # 
    aligned =    [b.id for b in all_bots if (b.alignment == 'aligned') ]
    misaligned = [b.id for b in all_bots if (b.alignment == 'misaligned')]
        
    # Start chat simulation
    manager = ChatroomManager(
        bots=all_bots,
        config=config,
        aligned_ids=aligned,
        misaligned_ids=misaligned
    )

    return manager.run_conversation_async(question)


def write_conversations_to_files(questions,finished_conversations,bots_per_question,path):

    # convos started in order, so can zip to keep questions where we finished a conversation.
    questions_and_convos = list(zip(questions,finished_conversations))
    base_dir = get_notebook_path()

    for i, (question, finished_convo) in enumerate(questions_and_convos):
    # Construct the output path
        all_bots = bots_per_question[i]

        # a little scuffed...
        aligned =    [b.id for b in all_bots if (b.alignment == 'aligned') ]
        misaligned = [b.id for b in all_bots if (b.alignment == 'misaligned')]

        topic_question = question['question']

        print(f"topic_question = {topic_question}")

        base_dir = get_notebook_path()
        output_path = base_dir / 'outputs' / 'Trial'/ f"{path}" 
                        
        generate_json_text_report(chat_history=finished_convo, 
                                    aligned_ids=aligned, 
                                    misaligned_ids=misaligned, 
                                    persuadable_ids=aligned,
                                    output_path=output_path,
                                    question_info=questions[i],
                                    question_number=i)
    
# example useage:

def write_conversation_to_file(question,finished_conversation,bots_for_question,path,question_number):

    # convos started in order, so can zip to keep questions where we finished a conversation.

    base_dir = get_notebook_path()

    # Construct the output path
    all_bots = bots_for_question

    # a little scuffed...
    aligned =    [b.id for b in all_bots if (b.alignment == 'aligned') ]
    misaligned = [b.id for b in all_bots if (b.alignment == 'misaligned')]

    topic_question = question['question']

    print(f"topic_question = {topic_question}")

    base_dir = get_notebook_path()
    output_path = base_dir / 'outputs' / 'Trial'/ f"{path}" 
                    
    generate_json_text_report(chat_history=finished_conversation, 
                                aligned_ids=aligned, 
                                misaligned_ids=misaligned, 
                                persuadable_ids=aligned,
                                output_path=output_path,
                                question_info=question,
                                question_number=question_number)
    


async def example(questions, num_to_ask):

    config = load_config('./config/config.yaml')

    all_bots_per_question = initialise_bots_for_questions(config, questions, num_to_ask)

    # this blocks until all conversations completed
    finished_conversations = run_questions_concurrently(config=config, questions=questions, num_to_ask=num_to_ask, all_bots_per_question=all_bots_per_question)

    write_conversations_to_files(questions, finished_conversations, all_bots_per_question)