import os
import json
from datetime import datetime
from typing import List, Dict, Any

CONVERSATION_DIR = "conversations"

def ensure_conversation_dir():
    if not os.path.exists(CONVERSATION_DIR):
        os.makedirs(CONVERSATION_DIR)

def new_conversation(environment_file: str, character_files: List[str]) -> Dict[str, Any]:
    """
    Create a new conversation structure.
    """
    ensure_conversation_dir()
    conversation = {
        "started_at": datetime.utcnow().isoformat(),
        "environment_file": environment_file,
        "character_files": character_files,
        "history": []
    }
    return conversation

def add_message(conversation: Dict[str, Any], role: str, content: str):
    """
    Add a message to the conversation history.
    """
    conversation["history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "role": role,
        "content": content
    })

def save_conversation(conversation: Dict[str, Any], filename: str = None):
    """
    Save the conversation to a file.
    If filename is not provided, auto-generate one.
    """
    ensure_conversation_dir()
    if not filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    if not filename.endswith('.json'):
        filename += '.json'
    filepath = os.path.join(CONVERSATION_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=2, ensure_ascii=False)

def load_conversation(filepath: str) -> Dict[str, Any]:
    """
    Load a conversation from a file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def list_conversations() -> List[str]:
    """
    List all conversation files.
    """
    ensure_conversation_dir()
    return [f for f in os.listdir(CONVERSATION_DIR) if f.endswith('.json')]