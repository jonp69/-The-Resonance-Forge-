import os
import json

ENVIRONMENT_FILE = "environment_prompt.json"
CHARACTER_DIR = "master_prompts"

class Environment:
    def __init__(self, title, synopsis, description, characters=None, tags=None, expected_model=None, **kwargs):
        self.title = title
        self.synopsis = synopsis
        self.description = description
        self.characters = characters or []
        self.tags = tags or []
        self.expected_model = expected_model
        # Accept and store any future metadata fields
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_json(cls, path=ENVIRONMENT_FILE):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Environment file '{path}' not found.")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

class Character:
    def __init__(self, name, synopsis, master_prompt, expected_model=None, **kwargs):
        self.name = name
        self.synopsis = synopsis
        self.master_prompt = master_prompt
        self.expected_model = expected_model
        # Accept and store any future metadata fields
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_json(cls, filename, directory=CHARACTER_DIR):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Character file '{path}' not found.")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    @classmethod
    def load_all(cls, directory=CHARACTER_DIR):
        characters = []
        if not os.path.isdir(directory):
            return characters
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                try:
                    character = cls.from_json(fname, directory)
                    characters.append(character)
                except Exception as e:
                    print(f"Warning: Failed to load character '{fname}': {e}")
        return characters

# Example usage:
# env = Environment.from_json()
# chars = Character.load_all()