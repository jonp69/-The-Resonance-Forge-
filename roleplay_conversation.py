import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"  # Example, replace with your LM Studio endpoint

def get_llm_response(prompt, backend="ollama", model="llama3"):
    if backend == "ollama":
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=data)
        return response.json()["response"]
    elif backend == "lmstudio":
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(LMSTUDIO_URL, json=data)
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise ValueError("Unknown backend selected.")

def main():
    backend = input("Select backend (ollama/lmstudio): ").strip().lower()
    model = input("Enter model name (e.g., llama3): ").strip()
    num_users = int(input("Number of users: "))
    num_characters = int(input("Number of roleplay characters: "))

    characters = []
    print("Define master prompts for each roleplay character:")
    for i in range(num_characters):
        prompt = input(f"Character {i+1} master prompt: ")
        characters.append({"name": f"Character_{i+1}", "prompt": prompt})

    users = []
    for i in range(num_users):
        name = input(f"Enter name for user {i+1}: ")
        users.append({"name": name})

    history = ""
    num_turns = int(input("How many turns in the conversation? "))

    for turn in range(num_turns):
        print(f"\n--- Turn {turn+1} ---")
        # Alternate between users and characters
        for participant in users + characters:
            if "prompt" in participant:  # character
                prompt = f"{history}\n{participant['name']} says (in character): {participant['prompt']}\n"
            else:  # user
                prompt = f"{history}\n{participant['name']}, enter your message: "
                user_message = input(prompt)
                history += f"{participant['name']}: {user_message}\n"
                continue  # users type their message directly

            response = get_llm_response(prompt, backend=backend, model=model)
            print(f"{participant['name']}: {response.strip()}")
            history += f"{participant['name']}: {response.strip()}\n"

if __name__ == "__main__":
    main()