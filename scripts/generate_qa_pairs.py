import json
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Replace with your key or use .env
model = genai.GenerativeModel('gemini-2.5-flash')  # Use correct model name

def generate_qa_pairs(section_id, section_text, max_pairs=20, max_text_length=4000):
    """
    Generate Q&A pairs for a given section using Gemini API.
    Args:
        section_id (str): Identifier of the section/act (e.g., 'Section 10').
        section_text (str): Text content of the section/act.
        max_pairs (int): Maximum number of Q&A pairs to generate.
        max_text_length (int): Maximum length of text to send to API to avoid token limits.
    Returns:
        list: List of dictionaries containing Q&A pairs.
    """
    act_name = "Inland Revenue (Amendment) Act, No. 2 of 2025"
    
    # Split long text into chunks to avoid token limits
    if len(section_text) > max_text_length:
        print(f"Warning: {section_id} text length ({len(section_text)}) exceeds {max_text_length}. Splitting into chunks.")
        text_chunks = [section_text[i:i + max_text_length] for i in range(0, len(section_text), max_text_length)]
    else:
        text_chunks = [section_text]
    
    all_qa_pairs = []
    
    for chunk_idx, chunk_text in enumerate(text_chunks, 1):
        prompt = f"""
        You are a legal expert in Sri Lankan business and corporate law. Based on the following text from {act_name}, generate {max_pairs // len(text_chunks)} high-quality, diverse, and relevant question-and-answer pairs that a business owner, lawyer, or student might ask. Ensure the questions are clear, legally accurate, and cover various aspects of the section (e.g., definitions, procedures, conditions, applications). In each question, explicitly reference '{section_id}' or '{act_name}' instead of vague terms like 'this section' or 'the act'. Provide concise answers that are directly based on the text.

        ### Section ID: {section_id}
        ### Section Text:
        {chunk_text}

        ### Output Format:
        Return a JSON array of objects, each containing a "question" and an "answer" field. The output must be valid JSON, wrapped in triple backticks (```json). Example:
        ```json
        [
            {{"question": "What is the purpose of {section_id} in {act_name}?", "answer": "{section_id} outlines..."}}
        ]
        ```
        Ensure the output is strictly valid JSON, with no additional text or comments outside the ```json``` block.
        """
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            print(f"Raw API response for {section_id} (chunk {chunk_idx}): {response_text}")  # Debug logging
            
            # Extract JSON from response
            if response_text.startswith("```json") and response_text.endswith("```"):
                json_text = response_text[7:-3].strip()
            else:
                json_text = response_text
            
            qa_pairs = json.loads(json_text)
            if not isinstance(qa_pairs, list):
                raise ValueError("API response is not a JSON array")
            for pair in qa_pairs:
                if not isinstance(pair, dict) or "question" not in pair or "answer" not in pair:
                    raise ValueError("Invalid Q&A pair format")
                # Ensure section/act name in question
                if "this section" in pair["question"].lower() or "the act" in pair["question"].lower():
                    raise ValueError(f"Question contains vague reference: {pair['question']}")
            all_qa_pairs.extend(qa_pairs)
        except Exception as e:
            print(f"Error generating Q&A for {section_id} (chunk {chunk_idx}): {e}")
            print(f"Retrying with stricter JSON enforcement...")
            
            # Retry with stricter prompt
            strict_prompt = f"{prompt}\n\nEnsure the output is strictly valid JSON, with no additional text or comments outside the ```json``` block. Avoid using 'this section' or 'the act' in questions."
            try:
                response = model.generate_content(strict_prompt)
                response_text = response.text.strip()
                print(f"Retry raw API response for {section_id} (chunk {chunk_idx}): {response_text}")
                if response_text.startswith("```json") and response_text.endswith("```"):
                    json_text = response_text[7:-3].strip()
                else:
                    json_text = response_text
                qa_pairs = json.loads(json_text)
                if not isinstance(qa_pairs, list):
                    raise ValueError("Retry API response is not a JSON array")
                for pair in qa_pairs:
                    if not isinstance(pair, dict) or "question" not in pair or "answer" not in pair:
                        raise ValueError("Invalid Q&A pair format in retry")
                    if "this section" in pair["question"].lower() or "the act" in pair["question"].lower():
                        raise ValueError(f"Question contains vague reference in retry: {pair['question']}")
                all_qa_pairs.extend(qa_pairs)
            except Exception as retry_e:
                print(f"Retry failed for {section_id} (chunk {chunk_idx}): {retry_e}")
                continue
    
    # Limit to max_pairs
    return all_qa_pairs[:max_pairs]

def main():
    # Load sections
    try:
        with open("data/output/sections.json", "r", encoding="utf-8") as f:
            sections = json.load(f)
    except Exception as e:
        print(f"Error loading sections.json: {e}")
        return {}
    
    # Generate Q&A pairs for each section
    qa_dataset = {}
    for section_id, section_text in sections.items():
        if not section_text.strip():
            print(f"Skipping {section_id}: Empty section text")
            qa_dataset[section_id] = []
            continue
        qa_pairs = generate_qa_pairs(section_id, section_text)
        qa_dataset[section_id] = qa_pairs
    
    # Save Q&A dataset
    try:
        with open("data/output/qa_dataset.json", "w", encoding="utf-8") as f:
            json.dump(qa_dataset, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving qa_dataset.json: {e}")
    
    return qa_dataset

if __name__ == "__main__":
    qa_dataset = main()
    print(f"Generated Q&A dataset saved to data/output/qa_dataset.json")