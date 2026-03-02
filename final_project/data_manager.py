import json
import os

# These are our "Save Files"
PANTRY_FILE = "pantry.json"
RECIPES_FILE = "recipes.json"
HISTORY_FILE = "history.json"

def load_data(filename):
    """Checks if a file exists and loads it; otherwise returns an empty dictionary."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(filename, data):
    """Writes the current Python dictionary back into the JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)