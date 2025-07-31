Legal LLM Phase 2: Q&A Dataset Generation
This project implements Phase 2 of the Legal Large Language Model (LLM) for Sri Lankan business and corporate law, focusing on generating a Q&A dataset from the Inland Revenue (Amendment) Act of Sri Lanka.
File Structure

scripts/: Python scripts for processing and generating Q&A pairs.
read_legal_text.py: Organizes JSON input into sections/acts.
generate_qa_pairs.py: Generates Q&A pairs using the Gemini API.
review_qa_pairs.py: Facilitates manual review and editing of Q&A pairs.
validate_qa_dataset.py: Validates the final Q&A dataset.


data/input/: Stores JSON input (e.g., cleaned_companies_act.json).
data/output/: Stores generated JSON files (sections.json, qa_dataset.json, reviewed_qa_dataset.json).
setup_environment.sh: Installs required Python libraries.
.env: Stores environment variables (e.g., Gemini API key).
README.md: This file.

Setup in VSCode

Clone the Repository:git clone <repository-url>
cd legal-llm-phase2


Create Virtual Environment:python -m venv venv
.\venv\Scripts\activate  # On Windows


Install Dependencies:bash setup_environment.sh


Configure API Key:
Edit .env to add your Gemini API key:GEMINI_API_KEY=your_api_key_here


Alternatively, set in VSCode’s launch.json:{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"GEMINI_API_KEY": "your_api_key_here"}
        }
    ]
}




Prepare Input Data:
Place the JSON input file in data/input/cleaned_companies_act.json.



Running the Pipeline

Read Legal Text:python scripts/read_legal_text.py


Output: data/output/sections.json


Generate Q&A Pairs:python scripts/generate_qa_pairs.py


Output: data/output/qa_dataset.json


Review Q&A Pairs:python scripts/review_qa_pairs.py


Output: data/output/reviewed_qa_dataset.json


Validate Dataset:python scripts/validate_qa_dataset.py



Notes

The input file (data/input/cleaned_companies_act.json) must be a valid JSON file with the structure shown in the project requirements.
Ensure the Gemini API key is valid and has sufficient quota.
Review Q&A pairs with a legal expert for accuracy.
The final reviewed_qa_dataset.json is ready for Phase 3 (model fine-tuning).
