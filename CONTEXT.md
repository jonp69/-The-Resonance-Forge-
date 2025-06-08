# Resonance Forge CONTEXT.md

## 1. File & Folder Structure

### 1.1 Master Prompts, Environments, Characters
- **Master prompts** are stored in a `master_prompts/` folder.
- **Environment/world prompts** are kept in `environments/` or `worlds/`.
- **Characters** are organized in `characters/`, with each character in its own subfolder if there are multiple variants.
    - Example: `characters/Alice/` might contain main, variants, archived, and sub-prompt files for Alice.

### 1.2 Variant & Archive Layout
- Each character/world/scenario file includes a `character_uuid` (or `world_uuid`, etc.) for the entity, and a `variant_uuid` for the specific file/version.
- Only one file per character UUID is marked as “main” and is placed at the root of its folder; other variants are placed in the `variants/` subfolder, archived ones in `archive/`.

### 1.3 Naming Consistency
- Filenames use a human-friendly name prefix and a truncated UUID (e.g., `Alice__b8f3d2e8.json`), but the full UUID is stored inside the file.
- Filenames and folders are for usability only; all identity and conflict logic is by UUID and content hash.

---

## 2. UUIDs, Variants, Duplicates, and Main File Rules

### 2.1 Character and Variant UUIDs

- **Every character** (or world, scenario) has a permanent `character_uuid` (`world_uuid`, etc.), RFC4122 v4.
- **Every file/variant** has a unique `variant_uuid`.
- The `character_uuid` links all files for that entity; the `variant_uuid` identifies each variant/version.

### 2.2 Main File Enforcement

- Only one “main” file per `character_uuid` can be active in the prompt set at a time.
- If loading another file with the same `character_uuid`, the user must:
    - Archive an existing main,
    - Make the new file a variant (assign new `variant_uuid`),
    - Or replace the main (archiving the old one).

### 2.3 True Duplicates, Distinct Variants

- **True duplicate:** Same `character_uuid`, same `variant_uuid`, same content hash.
    - User is notified: “You already have this character loaded (preexisting exact duplicate file detected).”
    - User can create a new variant or view info on the previous file.
- **Distinct variant:** Same `character_uuid`, different `variant_uuid` (content may overlap).
    - All variants (except main) are in `variants/`.
- File identity is never based on filename or location.

### 2.4 UUID Conflict Handling

1. **Detection:**  
   On load/import, scan for duplicate UUIDs. Compare content hashes.
2. **Impact Analysis:**  
   If any conflicting file’s hash was used in prior sessions/content generation, warn user and list affected outputs/conversations.
3. **Resolution Required:**  
   User must select which file to keep, fork (assign new `variant_uuid`), merge, or ignore for this session (with warnings if used in outputs).
4. **No Filename Reliance:**  
   Only UUIDs/hashes matter for identity/conflict.
5. **Session-Scoped Ignoring:**  
   Ignoring a conflict is valid only for current session; on next session, unresolved conflicts prompt again.

---

## 3. Prompt/Metadata Fields and UI/UX Requirements

### 3.1 Metadata Fields

- All prompt files include:
    - `character_uuid` or `world_uuid`
    - `variant_uuid`
    - `name`, `description`, `tags`
    - Version (`schema_version`)
    - `created_at`, `updated_at`
    - Optional: `legacy` (for deprecated fields), `forked_from` (for variants), `is_main` flag

### 3.2 UI/UX

- UI must display clear distinction between main files, variants, and archived.
- When a conflict or duplicate is detected, user is prompted with clear options and warnings.
- When generating new fields (migration or expansion), UI/LLM proposes values, user reviews/edits.

---

## 4. Migration, Legacy Fields, and Schema Evolution

### 4.1 Legacy Field Handling

- Removed fields are placed under a `"legacy"` key in the JSON.
- Legacy fields are accessed only for:
    - Manual edits,
    - Remigration,
    - Generating new fields/variants.
- Normal use ignores legacy fields.

### 4.2 New Field Acquisition (LLM-Driven, DRY)

- On schema upgrade or variant creation:
    1. System detects missing fields vs. schema.
    2. Prefills from legacy/related fields if available.
    3. Uses central field definition to build a context-rich prompt (using all available metadata).
    4. Calls the LLM to generate/suggest a value, which the user reviews, can iterate, and ultimately approves or edits.
    5. Field definition and prompt logic are centralized and DRY (single source of truth for prompting and requirements) for both migration and new content generation.

### 4.3 Renamed/Reworked Fields

- Versioned mapping table defines how old fields map to new for migration.
- Enables multi-version upgrades in one step.

---

## 5. Python Module & Folder Layout

- `resonance_forge/` is the main package.
    - `models/` – prompt and metadata schema classes.
    - `migration/` – schema versioning and migration logic.
    - `ui/` – user interface logic.
    - `storage/` – file I/O, archiving, hash/UUID checks.
    - `metadata/` – metadata collation and gathering utilities.
    - `llm/` – prompt builder and LLM client code.
    - `user_interaction/` – user review/iteration logic.
    - `workflows/` – high-level field autogeneration workflows.
    - `tests/` – test suite for all logic.
- Each LLM-reliant step is modularized for clarity, DRYness, and reuse across migration and content creation.

---

## 6. Sub-Prompts, Modifiers, and Character Expansion

- Sub-prompts/modifiers are stored as separate files in a `subprompts/` or `modifiers/` folder under each character.
- Each has its own `variant_uuid` and references its parent via `character_uuid` (and optionally `parent_variant_uuid`).
- Expansion logic for characters, worlds, and scenarios is unified: all use UUIDs, legacy handling, and migration logic as above.

---

## 7. Worlds, Environments, and Scenarios

- Same rules as for characters:
    - Unique `world_uuid`/`scenario_uuid`
    - Variants, main file enforcement, legacy handling, and migration logic all apply.
    - Filenames use truncated UUIDs for usability, with full UUID inside the file.

---

## 8. Naming, Consistency, and Best Practices

- All naming conventions (folders, files) aim for human usability but never replace UUID-based logic.
- Always prefer DRY for schema, field, and LLM prompt definitions.
- All user actions that affect data integrity (archival, variant creation, resolving conflicts) must be explicit and confirmed before changes are committed.

---

## 9. LLM-Driven Functionality: Consolidation & Flow

### 9.1 What Relies on LLMs
- Generating/suggesting values for new or missing fields (during migration or variant/content creation).
- Auto-generating descriptions, backstories, and other prompt content.
- Suggesting field autofill (traits, goals, etc.) based on metadata/context.
- Transforming/expanding legacy fields into new schema formats.
- Generating sub-prompts, modifiers, and creative expansions.

### 9.2 How It's Modularized (see code examples)
- `gather_metadata_for_query`: Collates all relevant metadata, legacy, and session context.
- `build_llm_query`: Builds a context-rich prompt using field definitions and metadata.
- `run_llm_query`: Loads and queries the LLM backend.
- `user_review_loop`: Lets the user review, edit, iterate, or accept generated content.
- `auto_generate_field`/`generate_missing_fields`: High-level workflow for filling in fields using the above, DRY for both migration and content creation.

---

## 10. Changelog

- **2025-06-08:** Integrated UUID/variant/duplicate logic, folder/file conventions, migration/legacy handling, and detailed LLM workflow modularization.

---

## 11. User Interface Architecture (PySide6)

### 11.1 GUI and Backend Separation
- The user interface is implemented using PySide6 (Qt for Python).
- All business logic, data processing, and workflows are kept in backend modules (e.g., `resonance_forge/`), with no direct UI dependencies.
- Each major backend module (LLM, metadata, workflows, etc.) may have a corresponding `gui_*.py` file or submodule for its UI components, but GUI and backend logic must remain decoupled.
- Communication between GUI and backend is via signals/slots, controller classes, or other clean interfaces.

### 11.2 Debug Console
- A parallel debug console is always available in the GUI for superuser access, internal state monitoring, and advanced debugging.
- The debug console can display logs, internal state, and allow for direct command input for power users.
- This enables advanced troubleshooting and development without overcomplicating the main user interface.

### 11.3 UI/UX Principles
- The GUI should be intuitive and user-friendly, with clear separation between normal user actions and advanced/superuser features.
- All user-facing workflows (e.g., missing file resolution, prompt review, conflict handling) are accessible via the GUI.
- The CLI interface may be retained for debugging, scripting, or headless operation, but the primary user experience is through the PySide6 GUI.

---

## 12. Core vs. Supporting Features in the GUI

### 12.1 Central Features (Core UX)

- The primary purpose of the GUI is to:
  - Allow the user to select and configure a local LLM backend (Ollama or LM Studio).
  - Let the user choose the number of users and roleplay characters, and select master prompts for each character.
  - Display and manage a conversation between users and roleplay characters, with clear message attribution.
  - Provide input fields for users to send messages as themselves or as a character.
  - Offer controls to start, pause, and reset the conversation.
- These features are always visible and form the main workflow of the application.

### 12.2 Supporting/Robustness Features

- Additional workflows (e.g., missing file resolution, prompt review, conflict handling) are available as modular dialogs or panels, but are not central to the main user flow.
- A debug console is available for superuser/internal state monitoring and troubleshooting, but is not the main focus for regular users.
- The GUI is designed so that robustness features enhance user satisfaction and reliability, but do not distract from the core conversation experience.

---

## 13. Conversation-Centric GUI and Dynamic State Management

### 13.1 Conversation as the Central Element
- The conversation log and message input are always visible and central in the GUI.
- LLM model selection, user/character management, and other settings are accessible via a sidebar, drawer, or modal, so they do not block or interrupt the conversation view.
- Users can change the LLM model or add/remove users/characters at any time, even mid-conversation.

### 13.2 Per-Interaction Registry
- Each message in the conversation log records:
  - Which LLM model was used for that interaction.
  - Which users and roleplay characters were present at that moment.
- This enables full traceability and reproducibility of the conversation.

### 13.3 Dynamic User/Character Management
- Users and characters can be added or removed at any time during the conversation.
- The current state (active users/characters) is checked and displayed at every interaction.
- The system ensures that all interactions are consistent with the current set of users/characters and the selected LLM.

### 13.4 Conversation Save File Metadata and Action System

- Each message/interaction in the saved conversation file includes metadata:
  - The LLM model used for that message
  - The users and roleplay characters present at that moment
- This metadata is for traceability and reproducibility, and is not displayed in the main conversation UI.
- Users and characters can have preset actions (e.g., join, leave, custom actions), which may be triggered at any time.
- Environments (ambients) can also define actions, and these may affect or be affected by user/character actions.
- The system supports triggering these actions, and their effects are reflected in the conversation state and saved in the conversation file.
- Environment-dependent actions and their effects are supported, allowing for dynamic and context-sensitive interactions.

---