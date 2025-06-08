def build_llm_query(metadata, field, field_defs):
    """
    Build a context-rich LLM prompt for generating/filling a specific field.
    - metadata: Dict from gather_metadata_for_query.
    - field: The target field to generate/suggest.
    - field_defs: Schema/definitions for fields.
    Returns: Prompt string for LLM.
    """
    field_info = field_defs.get(field, {})
    prompt = f"Given the following information about a character or entity:\n"
    for k, v in metadata.items():
        if k != "field_defs":
            prompt += f"- {k}: {v}\n"
    prompt += f"\nPlease generate a value for the '{field}' field."
    if "description" in field_info:
        prompt += f"\nField description: {field_info['description']}"
    if "requirements" in field_info:
        prompt += f"\nRequirements: {field_info['requirements']}"
    return prompt