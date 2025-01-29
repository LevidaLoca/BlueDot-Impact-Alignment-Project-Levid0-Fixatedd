from pathlib import Path

def generate_html_report(chat_history, aligned_ids, misaligned_ids, undermine_info, output_path):
    html_content = """
    <html>
    <head>
        <title>Chatroom Simulation Report</title>
        <style>
            .aligned { color: green; }
            .misaligned { color: red; }
        </style>
    </head>
    <body>
        <h1>Chatroom Simulation Report</h1>
        <p>Discussion topic: {}</p>
        <ul>
    """.format(undermine_info)
    
    for bot_id, response in chat_history:
        if bot_id in aligned_ids:
            html_content += '<li class="aligned">Bot {}: {}</li>'.format(bot_id, response)
        else:
            html_content += '<li class="misaligned">Bot {}: {}</li>'.format(bot_id, response)
    
    html_content += """
        </ul>
    </body>
    </html>
    """
    
    # Ensure the output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML content to the file
    with open(output_path, 'w') as f:
        f.write(html_content)
