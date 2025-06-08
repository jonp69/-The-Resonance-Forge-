def missing_file_menu():
    print("Missing required prompt file. What would you like to do?")
    print("A) Let program synthesize using context and your choice of LLM")
    print("B) Get a context-rich prompt to use with any LLM and import result")
    print("C) Import a prompt file manually")
    print("D) Cancel or choose a different prompt")
    choice = input("Select an option (A/B/C/D): ").strip().upper()
    return choice

def run_missing_file_workflow():
    choice = missing_file_menu()
    if choice == "A":
        print("Gathering context and available LLMs for assisted synthesis...")
        # Gather similar files, traits, tags, build prompt, let user pick LLM
        # Call LLM, present result for review
        print("Presenting generated prompt for review...")
    elif choice == "B":
        print("Generating a copyable prompt and context for manual LLM use...")
        # Gather context, build a prompt for user to paste into any LLM
        print("Paste generated result back or use 'Import' to load")
    elif choice == "C":
        print("Please select a prompt file to import.")
        # File dialog or path input here
    elif choice == "D":
        print("Cancelled. Please select or create another prompt.")
    else:
        print("Invalid option. Please try again.")