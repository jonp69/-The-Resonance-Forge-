import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QTextEdit, QComboBox, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt

# Import your loader and LLM interface modules
from prompt_loader import Environment, Character
from llm_interface import LLMInterface

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Resonance Forge Roleplay Engine")
        self.resize(900, 600)

        self.environment = None
        self.characters = []
        self.selected_characters = []
        self.llm = None
        self.model = None

        # UI Elements
        self.env_label = QLabel("Environment: (none loaded)")
        self.env_desc = QTextEdit()
        self.env_desc.setReadOnly(True)

        self.char_list = QListWidget()
        self.char_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_chars_btn = QPushButton("Reload Characters")
        self.load_env_btn = QPushButton("Reload Environment")

        self.backend_combo = QComboBox()
        self.backend_combo.addItems(["ollama", "lmstudio", "openai"])
        self.model_combo = QComboBox()
        self.load_models_btn = QPushButton("Reload Models")

        self.start_btn = QPushButton("Start Conversation")
        self.convo_view = QTextEdit()
        self.convo_view.setReadOnly(True)
        self.user_input = QTextEdit()
        self.send_btn = QPushButton("Send (as User)")
        self.send_rp_btn = QPushButton("Send (as Roleplay Character)")

        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        char_layout = QVBoxLayout()
        backend_layout = QHBoxLayout()
        convo_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        char_layout.addWidget(QLabel("Characters:"))
        char_layout.addWidget(self.char_list)
        char_layout.addWidget(self.load_chars_btn)
        char_layout.addWidget(self.load_env_btn)

        backend_layout.addWidget(QLabel("Backend:"))
        backend_layout.addWidget(self.backend_combo)
        backend_layout.addWidget(QLabel("Model:"))
        backend_layout.addWidget(self.model_combo)
        backend_layout.addWidget(self.load_models_btn)
        backend_layout.addStretch()

        top_layout.addWidget(self.env_label)
        top_layout.addWidget(self.env_desc)
        top_layout.addLayout(char_layout)

        convo_layout.addWidget(QLabel("Conversation:"))
        convo_layout.addWidget(self.convo_view)
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.send_rp_btn)
        convo_layout.addLayout(input_layout)
        convo_layout.addWidget(self.start_btn)

        main_layout.addLayout(backend_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(convo_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Signals
        self.load_chars_btn.clicked.connect(self.load_characters)
        self.load_env_btn.clicked.connect(self.load_environment)
        self.backend_combo.currentTextChanged.connect(self.reload_models)
        self.load_models_btn.clicked.connect(self.reload_models)
        self.start_btn.clicked.connect(self.start_conversation)
        self.send_btn.clicked.connect(self.send_user_message)
        self.send_rp_btn.clicked.connect(self.send_character_message)

        self.load_environment()
        self.load_characters()
        self.reload_models()

        self.history = []
        self.in_conversation = False

    def load_environment(self):
        try:
            self.environment = Environment.from_json()
            self.env_label.setText(f"Environment: {self.environment.title}")
            self.env_desc.setPlainText(f"{self.environment.synopsis}\n\n{self.environment.description}")
        except Exception as e:
            self.env_label.setText("Environment: (failed to load)")
            self.env_desc.setPlainText(str(e))

    def load_characters(self):
        self.characters = Character.load_all()
        self.char_list.clear()
        for char in self.characters:
            self.char_list.addItem(f"{char.name}: {char.synopsis}")

    def reload_models(self):
        backend = self.backend_combo.currentText()
        self.model_combo.clear()
        if backend == "ollama":
            # Try loading available models from Ollama
            try:
                models = LLMInterface.available_ollama_models()
                self.model_combo.addItems(models)
            except Exception:
                self.model_combo.addItem("llama3")
        elif backend == "lmstudio":
            # User must type in model for lmstudio, allow manual entry
            self.model_combo.setEditable(True)
            self.model_combo.addItem("llama3")
        elif backend == "openai":
            self.model_combo.setEditable(True)
            self.model_combo.addItem("gpt-3.5-turbo")
            self.model_combo.addItem("gpt-4")
        else:
            self.model_combo.addItem("llama3")

    def get_llm(self):
        backend = self.backend_combo.currentText()
        model = self.model_combo.currentText()
        if backend == "openai":
            key, ok = QInputDialog.getText(self, "OpenAI API Key", "Enter OpenAI API Key:", echo=QInputDialog.EchoMode.Password)
            if not ok:
                QMessageBox.warning(self, "Error", "OpenAI API key is required.")
                return None
            return LLMInterface(backend=backend, model=model, openai_api_key=key)
        return LLMInterface(backend=backend, model=model)

    def start_conversation(self):
        selected = self.char_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Characters", "Please select at least one character.")
            return
        self.selected_characters = [self.characters[self.char_list.row(item)] for item in selected]
        self.llm = self.get_llm()
        if not self.llm:
            return
        # Check for model compatibility
        for char in self.selected_characters:
            if char.expected_model and char.expected_model != self.model_combo.currentText():
                reply = QMessageBox.question(
                    self, "Model Mismatch",
                    f"Character {char.name} expects model '{char.expected_model}', but '{self.model_combo.currentText()}' is selected.\nContinue?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
        self.convo_view.clear()
        self.history = []
        self.in_conversation = True

    def send_user_message(self):
        if not self.in_conversation:
            QMessageBox.warning(self, "Not started", "Start a conversation first.")
            return
        text = self.user_input.toPlainText().strip()
        if not text:
            return
        self.history.append({"role": "User", "content": text})
        self.convo_view.append(f"<b>User:</b> {text}")
        self.user_input.clear()

    def send_character_message(self):
        if not self.in_conversation:
            QMessageBox.warning(self, "Not started", "Start a conversation first.")
            return
        # Choose which character to use for reply
        char_names = [char.name for char in self.selected_characters]
        char_idx, ok = QInputDialog.getItem(self, "Choose Character", "Roleplay as:", char_names, editable=False)
        if not ok:
            return
        char = self.selected_characters[char_names.index(char_idx)]
        # Compose prompt
        env = self.environment
        prompt = f"{env.synopsis}\n{env.description}\n\n{char.synopsis}\n{char.master_prompt}\n\nCurrent conversation history:\n"
        for entry in self.history:
            prompt += f"{entry['role']}: {entry['content']}\n"
        prompt += f"\n{char.name} responds:"
        self.convo_view.append(f"<i>Generating response as <b>{char.name}</b>...</i>")
        QApplication.processEvents()
        try:
            response = self.llm.get_response(prompt)
            self.convo_view.append(f"<b>{char.name}:</b> {response.strip()}")
            self.history.append({"role": char.name, "content": response.strip()})
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get response:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())