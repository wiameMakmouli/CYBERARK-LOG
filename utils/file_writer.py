import json

def write_json_logs(logs, filepath):
    with open(filepath, "w") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")
    print(f"Saved {len(logs)} logs to {filepath}")
