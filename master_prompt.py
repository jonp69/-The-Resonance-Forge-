import os
import json

PROMPT_DIR = "master_prompts"

def ensure_prompt_dir():
    if not os.path.exists(PROMPT_DIR):
        os.makedirs(PROMPT_DIR)

def list_prompts():
    ensure_prompt_dir()
    return [f for f in os.listdir(PROMPT_DIR) if f.endswith(".json")]

def save_prompt(prompt_data, filename=None):
    ensure_prompt_dir()
    fname = filename or f"{prompt_data['name'].replace(' ', '_')}.json"
    with open(os.path.join(PROMPT_DIR, fname), "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=2, ensure_ascii=False)

def load_prompt(filename):
    with open(os.path.join(PROMPT_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

def create_prompt_interactive(llm=None):
    print("=== Create New Master Prompt ===")
    name = input("Character name: ").strip()
    synopsis = input("Synopsis (leave empty to auto-generate): ").strip()
    if not synopsis and llm:
        desc_prompt = f"Write a short, vivid synopsis for a character based on the following master prompt."
        master_prompt = input("Enter the full master prompt: ").strip()
        synopsis = llm.get_response(f"{desc_prompt}\n\n{master_prompt}")
        print(f"Generated synopsis:\n{synopsis}\n")
    else:
        master_prompt = input("Enter the full master prompt: ").strip()

    model = input("Expected model for this prompt (e.g., llama3, phi3, gpt-4): ").strip()
    metadata = {
        "name": name,
        "synopsis": synopsis,
        "master_prompt": master_prompt,
        "expected_model": model
        # Add more fields as needed in the future
    }
    save_prompt(metadata)
    print(f"Prompt '{name}' saved.")
    return metadata