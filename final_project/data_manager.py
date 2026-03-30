import json
import os

# These are our "Save Files"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "assets", "data")

PANTRY_FILE = os.path.join(DATA_DIR, "pantry.json")
RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_data(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)