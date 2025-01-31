import os
import json

def run_judge(directory):
    # Construct the full path to the directory provided
    directory_fin = os.path.abspath(directory)

    files = os.listdir(directory_fin)
    print(range(len(files)))
    for i in range(len(files)):
        # Obligatory log file
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

if __name__ == "__main__":
    run_judge('C:/Users/pmyzl5/Desktop/Programming/BlueDot-Impact-Alignment-Project-Zachary-Levin/outputs/Trial')