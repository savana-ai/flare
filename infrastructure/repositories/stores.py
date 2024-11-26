import os
from infrastructure.repositories.json_repository import JSONRepository

# Determine the root project directory (adjust as needed)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ROOT_DIR, 'db')

# Ensure the db directory exists
os.makedirs(DB_PATH, exist_ok=True)

# Prompt templates using JSONRepository with full path
prompt_store = JSONRepository(os.path.join(DB_PATH, 'prompts.json'))

# Content store using JSONRepository with full path 
content_store = JSONRepository(os.path.join(DB_PATH, 'contents.json'))