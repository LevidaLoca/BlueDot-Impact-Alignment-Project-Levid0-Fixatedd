from pathlib import Path
import json
import datetime

def generate_text_report(chat_history, aligned_ids, misaligned_ids, undermine_info, output_path):
    report_content = (
        "Chatroom Simulation Report\n\n"
        f"Discussion topic: {undermine_info}\n\n"
        f"Aligned Bots: {aligned_ids}\n"
        f"Misaligned Bots: {misaligned_ids}\n\n"
    )
    
    for bot_id, response in chat_history:
        report_content += f"Participant {bot_id}: {response}\n\n"
    
    # Ensure the output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the report content to the file
    with open(output_path, 'w') as f:
        f.write(report_content)


def generate_json_text_report(chat_history, aligned_ids, misaligned_ids, persuadable_ids, output_path, question_info, question_number):

    date_time_string = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_name = f"{question_number}_{question_info['question']}_{date_time_string}"

    full_path = output_path/file_name

    bot_conversation = ""
    
    for bot_id, response in chat_history:
        bot_conversation += f"Participant {bot_id}: {response}\n\n"


    report_json = {
        "question_number": question_number,
        "question_info": question_info,
        "aligned_ids": aligned_ids,
        "misaligned_ids": misaligned_ids,
        "persuadable_ids": persuadable_ids,
        "chat_history": bot_conversation
        
    }
    
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=4, ensure_ascii=False)

    print(f"JSON report successfully saved to {full_path}")

    
    