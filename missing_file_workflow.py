# Backend logic for missing file workflow, separated from GUI
class MissingFileWorkflowBackend:
    def handle_choice(self, choice):
        if choice == "A":
            return "Gathering context and available LLMs for assisted synthesis..."
        elif choice == "B":
            return "Generating prompt and context for manual LLM use..."
        elif choice == "C":
            return "Please select a prompt file to import."
        elif choice == "D":
            return "Cancelled. Please select or create another prompt."
        else:
            return "Invalid option. Please try again."