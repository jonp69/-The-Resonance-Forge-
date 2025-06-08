import json, hashlib, os

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()

def check_file(path, registry_path="hash_registry.json"):
    if not os.path.exists(path):
        return "missing"
    file_hash = sha256_of_file(path)
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    known_hash = registry.get(path)
    if known_hash is None:
        return "unknown"
    elif file_hash == known_hash:
        return "healthy"
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            return "changed"
        except Exception:
            return "corrupt"