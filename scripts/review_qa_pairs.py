import json

def review_qa_pairs(input_file="data/output/qa_dataset.json", output_file="data/output/reviewed_qa_dataset.json"):
    """
    Facilitate manual review of Q&A pairs and save the refined dataset.
    Args:
        input_file (str): Path to the input Q&A dataset.
        output_file (str): Path to save the reviewed Q&A dataset.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        qa_dataset = json.load(f)
    
    reviewed_dataset = {}
    
    for section_id, qa_pairs in qa_dataset.items():
        print(f"\nReviewing Section: {section_id}")
        reviewed_pairs = []
        
        for i, pair in enumerate(qa_pairs, 1):
            print(f"\nQ&A Pair {i}:")
            print(f"Question: {pair['question']}")
            print(f"Answer: {pair['answer']}")
            action = input("Keep (k), Edit (e), Discard (d): ").lower()
            
            if action == 'k':
                reviewed_pairs.append(pair)
            elif action == 'e':
                new_question = input("Enter new question (or press Enter to keep): ").strip()
                new_answer = input("Enter new answer (or press Enter to keep): ").strip()
                edited_pair = {
                    "question": new_question if new_question else pair["question"],
                    "answer": new_answer if new_answer else pair["answer"]
                }
                reviewed_pairs.append(edited_pair)
            elif action == 'd':
                print("Pair discarded.")
            else:
                print("Invalid input, keeping pair.")
                reviewed_pairs.append(pair)
        
        reviewed_dataset[section_id] = reviewed_pairs
    
    # Save reviewed dataset
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviewed_dataset, f, indent=2, ensure_ascii=False)
    
    print(f"Reviewed Q&A dataset saved to {output_file}")

if __name__ == "__main__":
    review_qa_pairs()