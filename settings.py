import json
import os
import sys

# Determine where to save settings
if getattr(sys, 'frozen', False):
    # Running as .exe - save in AppData/Local/ClapCommander
    BASE_DIR = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ClapCommander')
    os.makedirs(BASE_DIR, exist_ok=True)
else:
    # Running as .py - save in script folder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")


def load_settings() -> dict:
    if not os.path.exists(SETTINGS_PATH):
        # Try to load defaults from bundled resources
        try:
            if getattr(sys, 'frozen', False):
                bundled = os.path.join(sys._MEIPASS, 'settings.json')
                if os.path.exists(bundled):
                    import shutil
                    shutil.copy(bundled, SETTINGS_PATH)
        except:
            pass
        if not os.path.exists(SETTINGS_PATH):
            return {}
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)


def save_settings(data: dict):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def get(key, default=None):
    settings = load_settings()
    return settings.get(key, default)