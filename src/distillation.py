from pathlib import Path

def generate_text_report(chat_history, aligned_ids, misaligned_ids, discussion_topic, output_path):
    report_content = (
        "Chatroom Simulation Report\n\n"
        f"Discussion topic: {discussion_topic}\n\n"
        f"Aligned Bots: {aligned_ids}\n"
        f"Misaligned Bots: {misaligned_ids}\n\n"
    )
    
    for bot_id, response in chat_history:
        report_content += f"Bot {bot_id}: {response}\n\n"
    
    # Ensure the output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the report content to the file
    with open(output_path, 'w') as f:
        f.write(report_content)
