import os
import json
from pathlib import Path

def run_judge(target_directory):
    print('hi')
    # Construct the full path to the directory provided
    # Step 1: Get the current working directory
    current_dir = Path.cwd()
    print(f"Current Working Directory: {current_dir}")

    # Step 2: Define the path to 'outputs/Trial/All_Aligned'
    directory_fin = current_dir / 'outputs' / 'Trial' / 'All_Aligned'
    print(f"Constructed Path: {directory_fin}")

    # Step 3: Create the directory if it doesn't exist
    directory_fin.mkdir(parents=True, exist_ok=True)
    print(f"Directory is ready at: {directory_fin.resolve()}")

    # Optional: Verify by listing contents
    print("\nContents of 'All_Aligned':")
    for item in directory_fin.iterdir():
        print(item)
    files = os.listdir(directory_fin)
    print(range(len(files)))
    for i in range(len(files)):

        print(f"Processing file {i+1}/{len(files)}: {files[i]}")
        
        # Store chat log from file
        file_path = os.path.join(directory_fin, files[i])
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Store question from file
            questions = data.get('questions', [])
            
            
            # Store answers
            # Store correct answers
            # Call API for truthful about there being misaligned
            # Call API for lying that there aren't misaligned
            # Call API for truthful about there aren't misaligned
            # Call API for lying that there are misaligned
    return False


