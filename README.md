# qanda-generation-component
Creating a supervised fine-tuning dataset consisting of question-answer pairs based on the prepared legal text.

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

Read Legal Text: - python scripts/read_legal_text.py
Generate Q&A Pairs: - python scripts/generate_qa_pairs.py
Review Q&A Pairs: - python scripts/review_qa_pairs.py
Validate Dataset: - python scripts/validate_qa_dataset.py
