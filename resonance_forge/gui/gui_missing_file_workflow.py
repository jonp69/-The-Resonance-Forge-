from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QDialogButtonBox)
from PySide6.QtCore import Signal, QObject

class MissingFileWorkflowBackend(QObject):
    # Signals for GUI to connect to
    state_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.state = "Waiting for user input."

    def handle_choice(self, choice):
        if choice == "A":
            self.state = "Gathering context and available LLMs for assisted synthesis..."
        elif choice == "B":
            self.state = "Generating prompt and context for manual LLM use..."
        elif choice == "C":
            self.state = "Please select a prompt file to import."
        elif choice == "D":
            self.state = "Cancelled. Please select or create another prompt."
        else:
            self.state = "Invalid option. Please try again."
        self.state_changed.emit(self.state)

class MissingFileWorkflowDialog(QDialog):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Missing File Workflow")
        layout = QVBoxLayout()
        self.label = QLabel("Missing required prompt file. Choose an option:")
        layout.addWidget(self.label)
        btn_layout = QHBoxLayout()
        self.btn_a = QPushButton("A) Synthesize with LLM")
        self.btn_b = QPushButton("B) Manual LLM Prompt")
        self.btn_c = QPushButton("C) Import File")
        self.btn_d = QPushButton("D) Cancel")
        for btn, code in zip([self.btn_a, self.btn_b, self.btn_c, self.btn_d], ["A", "B", "C", "D"]):
            btn.clicked.connect(lambda checked, c=code: self.on_choice(c))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        self.debug_console = QTextEdit()
        self.debug_console.setReadOnly(True)
        layout.addWidget(QLabel("Debug Console:"))
        layout.addWidget(self.debug_console)
        self.setLayout(layout)
        self.backend.state_changed.connect(self.update_debug_console)

    def on_choice(self, choice):
        self.backend.handle_choice(choice)

    def update_debug_console(self, state):
        self.debug_console.append(state)
