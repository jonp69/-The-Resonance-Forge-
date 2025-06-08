import requests

class LLMInterface:
    def __init__(self, backend="ollama", model="llama3", endpoint=None, openai_api_key=None):
        self.backend = backend.lower()
        self.model = model
        self.endpoint = endpoint
        self.openai_api_key = openai_api_key

    def get_response(self, prompt, history=None):
        if self.backend == "ollama":
            return self._ollama_generate(prompt, history)
        elif self.backend == "lmstudio":
            return self._lmstudio_generate(prompt, history)
        elif self.backend == "openai":
            return self._openai_generate(prompt, history)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

    def _ollama_generate(self, prompt, history):
        url = self.endpoint or "http://localhost:11434/api/generate"
        data = {
            "model": self.model,
            "prompt": self._format_history(prompt, history),
            "stream": False
        }
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()["response"]

    def _lmstudio_generate(self, prompt, history):
        url = self.endpoint or "http://localhost:1234/v1/chat/completions"
        data = {
            "model": self.model,
            "messages": self._build_messages(prompt, history)
        }
        resp = requests.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _openai_generate(self, prompt, history):
        url = self.endpoint or "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.openai_api_key}"}
        data = {
            "model": self.model,
            "messages": self._build_messages(prompt, history)
        }
        resp = requests.post(url, headers=headers, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _build_messages(self, prompt, history):
        messages = []
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        return messages

    def _format_history(self, prompt, history):
        if not history:
            return prompt
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + "\nUser: " + prompt

    @staticmethod
    def available_ollama_models(endpoint="http://localhost:11434/api/tags"):
        resp = requests.get(endpoint)
        resp.raise_for_status()
        tags = resp.json().get("models", [])
        return [m["name"] for m in tags]