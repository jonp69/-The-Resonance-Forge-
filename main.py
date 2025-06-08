import os
import sys
import time
from llm_interface import LLMInterface
from master_prompt import (
    list_prompts, load_prompt, create_prompt_interactive, PROMPT_DIR
)

def select_backend():
    print("Select backend:")
    print("1. Ollama")
    print("2. LM Studio")
    print("3. OpenAI-Compatible (untested)")
    try:
        choice = int(input("Enter number: ").strip())
    except ValueError:
        choice = 1
    if choice == 1:
        return "ollama"
    elif choice == 2:
        return "lmstudio"
    elif choice == 3:
        return "openai"
    else:
        return "ollama"

def get_model_for_backend(backend):
    if backend == "ollama":
        from llm_interface import LLMInterface
        models = LLMInterface.available_ollama_models()
        print(f"Available Ollama models: {models}")
        model = input("Model to use: ").strip()
        if not model or model not in models:
            print("Model not found, using 'llama3'.")
            return "llama3"
        return model
    elif backend == "lmstudio":
        model = input("Model to use for LM Studio (must be loaded in LM Studio): ").strip()
        return model or "llama3"
    elif backend == "openai":
        return input("OpenAI model (e.g., gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
    else:
        return "llama3"

def load_environment_prompt():
    with open("environment_prompt.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

def select_prompts():
    files = list_prompts()
    print("Available master prompts:")
    for i, fname in enumerate(files):
        print(f"{i+1}. {fname.replace('.json','')}")
    idxs = input("Enter comma-separated numbers of roleplay characters: ")
    idxs = [int(x.strip())-1 for x in idxs.split(",") if x.strip().isdigit()]
    prompts = [load_prompt(files[i]) for i in idxs]
    return prompts

def check_model_availability(expected_model, backend, llm):
    if backend == "ollama":
        available = LLMInterface.available_ollama_models()
        if expected_model not in available:
            print(f"Expected model '{expected_model}' not available in Ollama.")
            print("[1] Abort\n[2] Select different model\n[3] Install model and retry")
            c = input("Choice: ").strip()
            if c == "1":
                sys.exit(0)
            elif c == "2":
                return get_model_for_backend("ollama")
            elif c == "3":
                os.system(f"ollama pull {expected_model}")
                return expected_model
            else:
                sys.exit(0)
    # For LM Studio/OpenAI, just use the user-specified model for now
    return expected_model

def run():
    print("Welcome to The Resonance Forge Roleplay Engine!")
    if not os.path.exists(PROMPT_DIR):
        os.makedirs(PROMPT_DIR)
    if not os.path.exists("environment_prompt.txt"):
        print("Missing environment_prompt.txt. Please create it first.")
        sys.exit(1)

    backend = select_backend()
    model = get_model_for_backend(backend)
    openai_api_key = None
    if backend == "openai":
        openai_api_key = input("Enter OpenAI API key: ").strip()
    llm = LLMInterface(backend=backend, model=model, openai_api_key=openai_api_key)

    while True:
        print("\nMain Menu:")
        print("1. Start conversation")
        print("2. Create new master prompt")
        print("3. Exit")
        sel = input("Select: ").strip()
        if sel == "1":
            env_prompt = load_environment_prompt()
            prompts = select_prompts()
            # Check models
            for p in prompts:
                if "expected_model" in p and p["expected_model"] != model:
                    model = check_model_availability(p["expected_model"], backend, llm)
                    llm.model = model
            print("Enter number of users (humans):")
            n_users = int(input().strip())
            users = []
            for i in range(n_users):
                users.append(input(f"Enter user name {i+1}: ").strip())
            print("Conversation will now start. Type 'exit' to quit.\n")

            # Start conversation loop
            history = []
            turn = 0
            while True:
                print("\nConversation so far:")
                for entry in history:
                    print(f"{entry['role']}: {entry['content']}")
                print("\nWho speaks next?")
                for idx, u in enumerate(users):
                    print(f"{idx+1}. {u} (user)")
                for idx, p in enumerate(prompts):
                    print(f"{len(users)+idx+1}. {p['name']} (roleplay)")
                sel = input("Select: ").strip()
                if sel.lower() == "exit":
                    break
                try:
                    sel_idx = int(sel)-1
                except ValueError:
                    print("Invalid selection.")
                    continue
                if sel_idx < len(users):
                    msg = input(f"{users[sel_idx]}: ")
                    if msg.lower() == "exit":
                        break
                    history.append({"role": users[sel_idx], "content": msg})
                else:
                    p = prompts[sel_idx - len(users)]
                    prompt = f"{env_prompt}\n\n{p['synopsis']}\n{p['master_prompt']}\n\nCurrent conversation history:\n"
                    for entry in history:
                        prompt += f"{entry['role']}: {entry['content']}\n"
                    prompt += f"\n{p['name']} responds:"
                    print(f"Generating response as {p['name']}...")
                    response = llm.get_response(prompt)
                    print(f"{p['name']}: {response.strip()}")
                    history.append({"role": p['name'], "content": response.strip()})
        elif sel == "2":
            create_prompt_interactive(llm)
        elif sel == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run()