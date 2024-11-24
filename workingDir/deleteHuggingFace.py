from dotenv import load_dotenv
import os
from huggingface_hub import HfApi

# Load environment variables from .env file
load_dotenv()

# Access environment variables
hf_token = os.environ.get('HUGGINGFACE_TOKEN')
dataset_name = 'vihaannnn/Chunked-Indian-Supreme-Court-Judgements'
api = HfApi()

# Get the list of files in the repository
files = api.list_repo_files(repo_id=dataset_name, token=hf_token)

# Filter files matching the pattern "Recursive-Chunker-*"
files_to_delete = [file for file in files if file.startswith("Recursive-Chunker-")]

# Delete the filtered files
for file in files_to_delete:
    api.delete_file(path_in_repo=file, repo_id=dataset_name, token=hf_token)
    print(f"Deleted: {file}")

print("File deletion complete.")

