# Resonance Forge Prompt System

## Prompt Structure

- All character prompts in `character_prompts/`, filenames include name, version, traits.
- No world subfolders; instead, use `world_traits`, `compatible`, `incompatible`, `conditional` fields in JSON.
- Archived/old prompts in `archive/character_prompts/` (same filename convention).
- Raw prompts from external sources in `raw_prompts/`.

## Versioning & Integrity

- Each prompt has a `version` field.
- File hashes tracked in `hash_registry.json`.
- If a file changes, the user is prompted to register as new, recover, or review.
- Use `version_reader.py` to list all prompts and their info.

## Worlds

- World definitions in `worlds/`, each with a `traits` list.
- The program matches world traits to character tags for compatibility.

## Missing File Workflow

If a required file is missing:

A) Let program synthesize using context and your choice of LLM  
B) Get a context-rich prompt to use with any LLM and import result  
C) Import a prompt file manually  
D) Cancel or choose a different prompt  

## Usage

- Run `version_reader.py` to audit prompts.
- Use `file_integrity.py` to check prompt health.
- Use `missing_file_workflow.py` to resolve missing prompts.

## Example Character Prompt

```json
{
  "name": "Alice",
  "version": "2.0",
  "world_traits": ["modern", "urban", "no_magic", "high_tech"],
  "compatible": ["modern", "no_magic"],
  "incompatible": ["magic_only", "medieval"],
  "conditional": ["steampunk"],
  "tags": ["engineer", "inventor"],
  "notes": "If used in steampunk, swap 'laser gun' for 'steam blaster'.",
  "modifications": {
    "steampunk": {
      "description": "Replace modern tech with steam-powered gadgets."
    }
  }
}
```

---