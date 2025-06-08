# The Resonance Forge

**The Resonance Forge** is a local roleplay engine and conversation simulator for Python, with a GUI built using PySide6. It allows users to create, save, and replay rich, character-driven conversations powered by local LLMs such as Ollama, LM Studio, or optionally, OpenAI-compatible endpoints.

## Features

- **Modular LLM Backend**: Seamlessly switch between Ollama, LM Studio, or OpenAI-compatible APIs.
- **GUI Interface**: Manage environments, characters, and conversations with an intuitive PySide6 GUI.
- **Character & Environment Management**: Define and store roleplay characters (with metadata and master prompts) and environments in JSON.
- **Robust Conversation History**: Create, save, load, and automatically backup conversations.
- **Auto Dependency Handling**: Automatically install missing Python packages and restart the app as needed.
- **Extensible Data Model**: All prompts and environments stored as JSON for easy expansion and automation.

## Getting Started

### Prerequisites

- Python 3.9 or newer
- [Ollama](https://ollama.com/) and/or [LM Studio](https://lmstudio.ai/) (for local LLMs)
- (Optional) OpenAI API key for OpenAI endpoints

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jonp69/-The-Resonance-Forge-.git
   cd -The-Resonance-Forge-
   ```

2. **Install Python dependencies:**

   The application will attempt to auto-install dependencies (like PySide6) on first launch.  
   Alternatively, install them manually:

   ```bash
   pip install -r requirements.txt
   ```

   The main required packages:
   - `PySide6`
   - `requests`

3. **Run the Application:**

   ```bash
   python main_gui.py
   ```

   The GUI will launch. If dependencies are missing, you'll be prompted to install them.

### Directory Structure

```
.
├── autopip.py           # Auto pip install & restart logic
├── conversation_io.py   # Conversation saving/loading/undo
├── llm_interface.py     # Unified interface for Ollama, LM Studio, OpenAI
├── main_gui.py          # Main PySide6 GUI
├── master_prompt.py     # Character metadata and prompt management
├── prompt_loader.py     # Data classes for environments and characters
├── master_prompts/      # Folder for character prompt JSONs
├── conversations/       # Saved conversations and backups
├── environment_prompt.json # Example environment prompt (JSON with metadata)
├── requirements.txt     # List of Python dependencies
└── README.md
```

## Usage

1. **Launch the GUI** (`python main_gui.py`).
2. **Select or create environments and characters** using the lists.
3. **Start a new conversation** or load an existing one.
4. **Interact as users and/or characters**. The conversation is backed up automatically.
5. **Save or restore conversations** as needed.

### Adding Characters or Environments

- Place character JSON files in `master_prompts/`.
- Place environment JSON files (e.g. `environment_prompt.json`) in the main directory.

### OpenAI API

If using the OpenAI backend, you will be prompted for your API key at runtime.

## Contributing

Pull requests and suggestions are welcome!  
Please ensure your code is well-documented and tested.

## License

MIT License

---

**Enjoy building stories and worlds with The Resonance Forge!**