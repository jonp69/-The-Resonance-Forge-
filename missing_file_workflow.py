def missing_file_menu():
    print("Missing required prompt file. Choose an option:")
    print("A) Synthesize using context and LLM of your choice")
    print("B) Get a context-rich prompt for any LLM, import result")
    print("C) Import a file manually")
    print("D) Cancel / Try a different prompt")
    choice = input("Select (A/B/C/D): ").strip().upper()
    return choice

def run_missing_file_workflow():
    choice = missing_file_menu()
    if choice == "A":
        print("Gathering context and available LLMs for assisted synthesis...")
        # Implement: gather context, pick LLM, call LLM, present result
    elif choice == "B":
        print("Generating prompt and context for manual LLM use...")
        # Implement: show prompt, user pastes into LLM, then imports
    elif choice == "C":
        print("Please select a prompt file to import.")
        # Implement: file picker or path input
    elif choice == "D":
        print("Cancelled. Please select or create another prompt.")
    else:
        print("Invalid option. Please try again.")