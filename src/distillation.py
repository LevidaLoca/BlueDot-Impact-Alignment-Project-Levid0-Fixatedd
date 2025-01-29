from datetime import datetime
import os

def generate_html_report(chat_history, aligned, misaligned, topic, output_path):
    html = f"""
    <html>
    <head>
        <title>Chatroom Simulation Report</title>
        <style>
            .message {{ margin: 10px; padding: 8px; border-radius: 5px; }}
            .aligned {{ background: #e8f5e9; border-left: 4px solid #2e7d32; }}
            .misaligned {{ background: #ffebee; border-left: 4px solid #c62828; }}
            .meta {{ color: #666; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>Discussion Topic: {topic}</h1>
        <div class="meta">
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | 
            Aligned: {len(aligned)} bots | Misaligned: {len(misaligned)}
        </div>
        <hr>
    """
    
    for entry in chat_history:
        bot_id, response = entry['bot_id'], entry['response']
        cls = "misaligned" if bot_id in misaligned else "aligned"
        html += f"""
        <div class="message {cls}">
            <strong>Bot #{bot_id}:</strong> {response}
        </div>
        """
    
    html += "</body></html>"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)