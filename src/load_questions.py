import json
from datasets import load_dataset

class TruthfulQADataLoader:
    def __init__(self):
        """
        Initializes an empty TruthfulQA data loader instance.
        Does NOT download the dataset automatically.
        """
        self.questions = []  # Stores loaded questions

    def load_data_from_huggingface(self, split="validation"):
        """
        Downloads the TruthfulQA dataset from Hugging Face, processes it,
        and loads it into the instance variable `self.questions`.

        :param split: The dataset split to load ('train' or 'validation'). Default is 'validation'.
        """
        print(f"Downloading the TruthfulQA dataset ({split} split)...")
        dataset = load_dataset("truthful_qa", "multiple_choice")[split]

        self.questions = []  # Clear existing data

        for item in dataset:
            question_text = item['question']
            mc_answers = item['mc1_targets']['choices']

            # Get correct answers
            correct_answer_indices = item['mc1_targets']['labels']
            correct_answers = [mc_answers[i] for i in correct_answer_indices]

            # Get best incorrect answer
            best_wrong_idx = item['mc1_targets'].get('best_wrong_idx', None)
            best_incorrect_answer = None
            if isinstance(best_wrong_idx, int) and 0 <= best_wrong_idx < len(mc_answers):
                best_incorrect_answer = mc_answers[best_wrong_idx]
            else:
                # If no "best wrong answer" exists, pick the first incorrect answer arbitrarily
                incorrect_answers = [mc_answers[i] for i in range(len(mc_answers)) if i not in correct_answer_indices]
                best_incorrect_answer = incorrect_answers[0] if incorrect_answers else None  # Ensure there's at least one incorrect answer



            # Get all incorrect answers (excluding correct ones)
            incorrect_answers = [mc_answers[i] for i in range(len(mc_answers)) if i not in correct_answer_indices]

            self.questions.append({
                "question": question_text,
                "choices": mc_answers,
                "correct_answers": correct_answers,
                "incorrect_answers": incorrect_answers,
                "best_incorrect_answer": best_incorrect_answer
            })

        print(f"Successfully loaded {len(self.questions)} questions from Hugging Face.")

    def save_to_json(self, filename="truthful_qa_questions.json"):
        """
        Saves the loaded questions to a JSON file.

        :param filename: The name of the JSON file to save the data.
        """
        if not self.questions:
            print("No data to save! Load or process questions first.")
            return
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(self.questions)} questions to '{filename}'")

    @staticmethod
    def load_from_json(filename):
        """
        Loads a JSON file containing TruthfulQA data.

        :param filename: The JSON file to load.
        :return: List of dictionaries with question data.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Successfully loaded {len(data)} questions from '{filename}'")
            return data
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{filename}'.")
            return []

# # Example usage
# if __name__ == "__main__":
#     loader = TruthfulQADataLoader()

#     # Example: Load from a JSON file instead of downloading
#     loaded_data = loader.load_from_json("truthful_qa_with_incorrect_answers.json")

#     # Assign loaded data to the class instance
#     loader.questions = loaded_data

#     # Save to another JSON file (if needed)
#     loader.save_to_json("backup_truthful_qa.json")

#     # Print
