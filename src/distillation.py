from pathlib import Path

def generate_text_report(chat_history, aligned_ids, misaligned_ids, undermine_info, output_path):
    report_content = f"Chatroom Simulation Report\n\nDiscussion topic: {undermine_info}\n\n"
    
    for bot_id, response in chat_history:
        if bot_id in aligned_ids:
            report_content += f"Aligned Bot {bot_id}: {response}\n"
        else:
            report_content += f"Misaligned Bot {bot_id}: {response}\n"
    
    # Ensure the output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the report content to the file
    with open(output_path, 'w') as f:
        f.write(report_content)

# Example usage
if __name__ == "__main__":
    chat_history = [(0, "This is a test response from an aligned bot."), (1, "This is a test response from a misaligned bot.")]
    aligned_ids = [0]
    misaligned_ids = [1]
    undermine_info = "Solar power is harmful to the sun"
    output_path = Path(__file__).parent.parent / 'outputs' / 'chat_logs' / 'report.txt'
    generate_text_report(chat_history, aligned_ids, misaligned_ids, undermine_info, output_path)