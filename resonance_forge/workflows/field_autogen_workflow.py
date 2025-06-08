from resonance_forge.metadata.metadata_utils import gather_metadata_for_query
from resonance_forge.llm.llm_prompt_builder import build_llm_query
from resonance_forge.llm.llm_client import LLMClient
from resonance_forge.user_interaction.user_review import user_review_loop

def auto_generate_field(field, file_data, legacy_data, session_data, field_defs, llm_client):
    """
    Full workflow for generating a missing field value.
    Returns: User-approved value for field.
    """
    metadata = gather_metadata_for_query(file_data, legacy_data, session_data, field_defs)
    prompt = build_llm_query(metadata, field, field_defs)
    initial_value = llm_client.run_llm_query(prompt)
    final_value = user_review_loop(field, initial_value, metadata, llm_client, field_defs)
    return final_value

def generate_missing_fields(file_data, legacy_data, session_data, field_defs, llm_client):
    """
    Fills all missing fields in file_data by invoking auto_generate_field.
    Returns: Updated file_data with all missing fields filled.
    """
    updated = file_data.copy()
    for field in field_defs:
        if field not in file_data or not file_data[field]:
            value = auto_generate_field(field, updated, legacy_data, session_data, field_defs, llm_client)
            updated[field] = value
    return updated