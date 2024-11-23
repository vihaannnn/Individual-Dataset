from dotenv import load_dotenv
import os
from huggingface_hub import HfApi

# Load environment variables from .env file
load_dotenv()

# Access environment variables
hf_token = os.environ.get('HUGGINGFACE_TOKEN')
dataset_name = 'vihaannnn/Indian-Supreme-Court-Judgements-Chunked'
local_folder_path = '../Chunked'
# Initialize Hugging Face API
api = HfApi()

# Upload folder to Hugging Face dataset
api.upload_folder(
    folder_path=local_folder_path,
    repo_id=dataset_name,
    repo_type="dataset",
    token=hf_token
)

print(f"Folder {local_folder_path} uploaded to {dataset_name} dataset successfully.")