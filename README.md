# The Resonance Forge

**The Resonance Forge** is a local roleplay engine and conversation simulator for Python, with a GUI built using PySide6. It allows users to create, save, and replay rich, character-driven conversations powered by large language models (LLMs) served locally via frameworks such as Ollama and LM Studio, or optionally through OpenAI-compatible endpoints.

## Features

- **Modular LLM Backend**: Seamlessly switch between local LLM server frameworks such as Ollama, LM Studio (which host a variety of models), or OpenAI-compatible APIs.
- **GUI Interface**: Manage environments, characters, and conversations with an intuitive PySide6 GUI.
- **Character & Environment Management**: Define and store roleplay characters (with metadata and master prompts) and environments in JSON.
- **Robust Conversation History**: Create, save, load, and automatically backup conversations, with undo/restore support.
- **Auto Dependency Handling**: Automatically install missing Python packages and restart the app as needed.
- **Extensible Data Model**: All prompts and environments are stored as JSON for easy expansion and automation.

## Getting Started

### Prerequisites

- Python 3.9 or newer
- [Ollama](https://ollama.com/) and/or [LM Studio](https://lmstudio.ai/) (for local LLM serving)
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
├── autopip.py                  # Auto pip install & restart logic
├── conversation_io.py          # Conversation saving/loading/undo with backup support
├── llm_interface.py            # Unified interface for Ollama, LM Studio, OpenAI
├── main_gui.py                 # Main PySide6 GUI
├── master_prompt.py            # Character metadata and prompt management
├── prompt_loader.py            # Data classes for environments and characters
├── character_prompts/          # Folder for character prompts (master and modifiers)
│   ├── Alice.json              # Master character prompt for Alice
│   ├── Alice/                  # Subfolder for Alice's modifier/sub-prompts
│   │   ├── friendly.json
│   │   └── angry.json
│   ├── Bob.json
│   └── Bob/
│       └── excited.json
├── environment_prompts/        # Folder for environment prompt JSONs
│   └── The_Resonance_Game.json # Example environment prompt for the project
├── conversations/              # Saved conversations and backups
├── requirements.txt            # List of Python dependencies
└── README.md
```

## Usage

1. **Launch the GUI** (`python main_gui.py`).
2. **Select or create environments and characters** using the lists.
3. **Start a new conversation** or load an existing one.
4. **Interact as users and/or characters**. The conversation is backed up automatically and can be restored if needed.
5. **Save or restore conversations** as needed.

### Adding Characters or Environments

- Place master character JSON files in `character_prompts/` (e.g. `Alice.json`).
- For each character, create a subfolder under `character_prompts/` (e.g. `character_prompts/Alice/`) containing modifier or sub-prompt JSON files.
- Place environment JSON files in `environment_prompts/`. For example, an environment for this project might be named `The_Resonance_Game.json`.

### Using Local LLMs

- **Ollama** and **LM Studio** are not LLMs themselves, but server frameworks that allow you to run a variety of large language models (e.g., Llama 3, Phi-3) on your own hardware.  
- This project connects to these servers, sending prompts and receiving responses from the models you have loaded.

### OpenAI API

If using the OpenAI backend, you will be prompted for your API key at runtime.

## Contributing

Pull requests and suggestions are welcome!  
Please ensure your code is well-documented and tested.

## License

MIT License

---

**Enjoy building stories and worlds with The Resonance Forge!**