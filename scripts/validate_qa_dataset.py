import json

def validate_qa_dataset(file_path="data/output/reviewed_qa_dataset.json", min_pairs_per_section=15):
    """
    Validate the structure and content of the Q&A dataset.
    Args:
        file_path (str): Path to the Q&A dataset JSON file.
        min_pairs_per_section (int): Minimum number of Q&A pairs required per section.
    Returns:
        bool: True if validation passes, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            qa_dataset = json.load(f)
    except Exception as e:
        print(f"Error: Failed to load {file_path}: {e}")
        print("Suggestion: Ensure the file exists and contains valid JSON. Check for syntax errors using a JSON validator.")
        return False

    errors = []
    summary = {}
    
    # Check if dataset is a dictionary
    if not isinstance(qa_dataset, dict):
        errors.append("Error: Dataset is not a JSON object (dictionary). Expected format: { 'Section X': [...] }")
        return False
    
    # Validate each section
    for section_id, qa_pairs in qa_dataset.items():
        summary[section_id] = len(qa_pairs)
        
        # Check if section has Q&A pairs
        if not qa_pairs:
            errors.append(f"Section {section_id}: No Q&A pairs found. Expected at least {min_pairs_per_section} pairs.")
            continue
        
        # Check number of pairs
        if len(qa_pairs) < min_pairs_per_section:
            errors.append(f"Section {section_id}: Only {len(qa_pairs)} Q&A pairs found. Expected at least {min_pairs_per_section} pairs.")
        
        # Validate each Q&A pair
        for i, pair in enumerate(qa_pairs, 1):
            # Check if pair is a dictionary
            if not isinstance(pair, dict):
                errors.append(f"Section {section_id}, pair {i}: Not a dictionary. Expected format: {{'question': '...', 'answer': '...'}}")
                continue
            
            # Check for required fields
            if "question" not in pair or "answer" not in pair:
                errors.append(f"Section {section_id}, pair {i}: Missing 'question' or 'answer' field.")
                continue
            
            # Check for non-empty fields
            if not pair["question"].strip():
                errors.append(f"Section {section_id}, pair {i}: Question is empty or contains only whitespace.")
            if not pair["answer"].strip():
                errors.append(f"Section {section_id}, pair {i}: Answer is empty or contains only whitespace.")
            
            # Check for minimum content length (heuristic for meaningful content)
            if len(pair["question"].strip()) < 10:
                errors.append(f"Section {section_id}, pair {i}: Question is too short (less than 10 characters). Consider rephrasing for clarity.")
            if len(pair["answer"].strip()) < 10:
                errors.append(f"Section {section_id}, pair {i}: Answer is too short (less than 10 characters). Consider providing more detail.")

    # Print summary
    print("\nDataset Summary:")
    for section_id, count in summary.items():
        print(f"{section_id}: {count} Q&A pairs")
    
    # Print validation results
    if errors:
        print("\nValidation Errors Found:")
        for error in errors:
            print(error)
        print("\nSuggestions:")
        print("- If sections have too few pairs, re-run generate_qa_pairs.py with a higher max_pairs value or generate additional pairs.")
        print("- If pairs are malformed or empty, re-run review_qa_pairs.py to edit or discard problematic pairs.")
        print("- Verify legal accuracy with an expert, especially for sections with complex amendments (e.g., Section 2).")
        return False
    else:
        print("\nQ&A dataset validated successfully.")
        print("Next Steps: The dataset is ready for Phase 3 (model fine-tuning). Share reviewed_qa_dataset.json with the Model/MLOps Team.")
        return True

if __name__ == "__main__":
    validate_qa_dataset()