import os, json

def scan_prompts(root_folder):
    results = []
    for dirpath, _, filenames in os.walk(root_folder):
        for fname in filenames:
            if fname.endswith(".json"):
                full_path = os.path.join(dirpath, fname)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    name = data.get("name", "Unknown")
                    version = data.get("version", "Unknown")
                    world = ", ".join(data.get("world_traits", []))
                    results.append({
                        "file": full_path,
                        "name": name,
                        "world": world,
                        "version": version
                    })
                except Exception as e:
                    results.append({"file": full_path, "name": "Unreadable", "world": "-", "version": "-"})
    return results

def print_table(results):
    print(f"{'File':40} {'Character':12} {'World(s)':20} {'Version':8}")
    print("-" * 80)
    for r in results:
        print(f"{r['file'][:40]:40} {r['name'][:12]:12} {r['world'][:20]:20} {r['version'][:8]}")

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "character_prompts"
    results = scan_prompts(folder)
    print_table(results)