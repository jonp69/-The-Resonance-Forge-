def user_review_loop(field, initial_value, metadata, llm_client, field_defs):
    """
    UX loop for reviewing/editing LLM-generated value.
    - field: Target field name.
    - initial_value: LLM's initial suggestion.
    - metadata: For context display.
    - llm_client: For requesting alternates.
    - field_defs: For field help text.
    Returns: Final user-approved value.
    """
    print(f"Suggested value for '{field}':\n{initial_value}\n")
    while True:
        action = input("Accept (a), Edit (e), Retry (r), Show Context (c), Show Help (h), Quit (q): ").strip().lower()
        if action == "a":
            return initial_value
        elif action == "e":
            edited = input("Enter your edited value: ")
            return edited
        elif action == "r":
            # Request alternate suggestion from LLM
            prompt = build_llm_query(metadata, field, field_defs)
            initial_value = llm_client.run_llm_query(prompt)
            print(f"\nAlternate suggestion:\n{initial_value}\n")
        elif action == "c":
            print("Context used for generation:")
            for k, v in metadata.items():
                print(f"- {k}: {v}")
        elif action == "h":
            print(f"Help for '{field}': {field_defs.get(field, {}).get('description','No help available.')}")
        elif action == "q":
            print("Quitting review loop.")
            break