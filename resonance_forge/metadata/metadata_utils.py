def gather_metadata_for_query(file_data, legacy_data=None, session_data=None, field_defs=None):
    """
    Collate all relevant metadata for a field, drawing from:
    - Main file metadata (file_data)
    - Legacy/deprecated fields (legacy_data)
    - Session/conversation context (session_data)
    - Field definitions/schema (field_defs)
    Returns a single dict for prompt construction.
    """
    metadata = {}
    metadata.update(file_data or {})
    if legacy_data:
        metadata['legacy'] = legacy_data
    if session_data:
        metadata['session'] = session_data
    if field_defs:
        metadata['field_defs'] = field_defs
    return metadata