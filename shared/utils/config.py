import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Finds the project root by looking for the .git directory and loads the .env file.
    """
    # Start from the current file's directory and go up
    current_path = Path(__file__).parent
    project_root = None

    # Search for the .git directory as a marker for the project root
    for parent in [current_path] + list(current_path.parents):
        if (parent / ".git").is_dir():
            project_root = parent
            break
    
    if project_root:
        dotenv_path = project_root / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)
        else:
            print(f"Warning: .env file not found at {dotenv_path}")
    else:
        print("Warning: Project root with .git directory not found. Could not load .env file.")

# Automatically load the environment when this module is imported
load_environment()
