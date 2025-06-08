# resonance_forge/conversation/conversation_tree.py
"""
ConversationTree: Data structure for managing conversation history, alternative messages, and branching.
"""
from typing import List, Optional, Dict, Any
import uuid

class ConversationNode:
    def __init__(self, message: str, sender: str, metadata: dict, parent: Optional['ConversationNode']=None):
        self.id = str(uuid.uuid4())
        self.message = message
        self.sender = sender
        self.metadata = metadata  # e.g., LLM used, users/characters present, settings
        self.parent = parent
        self.children: List['ConversationNode'] = []  # Alternatives/branches
        self.audio_path: Optional[str] = None  # For TTS/audio
        self.timestamp = metadata.get('timestamp')

    def add_child(self, node: 'ConversationNode'):
        self.children.append(node)
        node.parent = self

    def get_path(self) -> List['ConversationNode']:
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'message': self.message,
            'sender': self.sender,
            'metadata': self.metadata,
            'audio_path': self.audio_path,
            'timestamp': self.timestamp,
            'children': [child.to_dict() for child in self.children]
        }

class ConversationTree:
    def __init__(self):
        self.root = ConversationNode("Conversation Start", "system", {}, None)
        self.current = self.root

    def add_message(self, message: str, sender: str, metadata: dict, as_alternative=False):
        node = ConversationNode(message, sender, metadata, None)
        if as_alternative and self.current.parent:
            self.current.parent.add_child(node)
        else:
            self.current.add_child(node)
            self.current = node
        return node

    def undo_to(self, node_id: str):
        # Set current to the node with node_id, remove all descendants
        node = self.find_node(self.root, node_id)
        if node:
            node.children = []
            self.current = node

    def find_node(self, node: ConversationNode, node_id: str) -> Optional[ConversationNode]:
        if node.id == node_id:
            return node
        for child in node.children:
            found = self.find_node(child, node_id)
            if found:
                return found
        return None

    def to_dict(self):
        return self.root.to_dict()

    def get_all_paths(self) -> List[List[ConversationNode]]:
        # Returns all possible conversation paths (for navigation/playback)
        def dfs(node, path, paths):
            path.append(node)
            if not node.children:
                paths.append(list(path))
            else:
                for child in node.children:
                    dfs(child, path, paths)
            path.pop()
        paths = []
        dfs(self.root, [], paths)
        return paths
