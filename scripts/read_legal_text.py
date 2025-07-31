import json
import os

def read_legal_text(input_path):
    """
    Read and organize legal text from a JSON input file into sections.
    Args:
        input_path (str): Path to the JSON input file.
    Returns:
        dict: Dictionary with section identifiers as keys and concatenated text content as values.
    """
    sections = {}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for section in data:
        section_id = f"Section {section['section_number']}"
        section_content = []
        
        # Handle basic section content (subsections)
        if 'content' in section:
            for subsection in section['content']:
                section_content.append(subsection['text'])
        
        # Handle amendments if present
        if 'amendments' in section:
            for amendment in section['amendments']:
                if 'changes' in amendment:
                    for change in amendment['changes']:
                        if 'original_text' in change and 'new_text' in change:
                            section_content.append(f"Amendment to {section.get('amendment_to', 'unknown section')}, paragraph {amendment.get('paragraph', 'unknown')}: Changed '{change['original_text']}' to '{change['new_text']}'.")
                if 'text' in amendment:
                    section_content.append(amendment['text'])
                    if 'conditions' in amendment:
                        section_content.append("Conditions: " + "; ".join(amendment['conditions']))
        
        # Join all content for the section
        sections[section_id] = " ".join(section_content)
    
    return sections

if __name__ == "__main__":
    input_path = "data/input/cleaned_companies_act.json"
    sections = read_legal_text(input_path)
    with open("data/output/sections.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    print(f"Sections saved to data/output/sections.json")