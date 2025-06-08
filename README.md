# Resonance Forge Prompt System

## Structure

- All character prompts in `character_prompts/`, filenames include name, version, traits.
- No world subfolders; use `world_traits`, `compatible`, `incompatible`, `conditional` fields in JSON.
- Archived/old prompts in `archive/character_prompts/`.
- Raw prompts from external sources in `raw_prompts/`.

## Versioning & Integrity

- Each prompt has a `version` field.
- File hashes in `hash_registry.json`.
- If a file changes, user is prompted to register as new, recover, or review.
- Run `version_reader.py` to audit prompts.

## Worlds

- World definitions in `worlds/`, each with a `traits` list.
- Program matches world traits to character tags for compatibility.

## Missing File Workflow

A) Synthesize using context and LLM of your choice  
B) Get a context-rich prompt for any LLM, import result  
C) Import a file manually  
D) Cancel / Try a different prompt  

## Usage

- Run `version_reader.py` to list prompts.
- Use `file_integrity.py` to check prompt health.
- Use `missing_file_workflow.py` for missing prompts.

## Example Prompt

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