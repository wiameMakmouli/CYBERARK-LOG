from datetime import datetime

def normalize_to_ecs(log):
    return {
        "@timestamp": log.get("timestamp", datetime.utcnow().isoformat()),
        "event": {
            "action": log.get("action", "unknown").lower(),
            "category": ["authentication", "session"],
            "outcome": "success" if log.get("action") == "Logon" else "unknown",
            "type": ["start"] if log.get("action") == "Logon" else ["info"]
        },
        "user": {
            "name": log.get("username", log.get("issuer"))
        },
        "host": {
            "name": "VAULT"
        },
        "source": {
            "ip": log.get("station", "0.0.0.0")
        },
        "cyberarkpas": {
            "audit": log
        },
        "tags": ["cyberarkpas-audit", "forwarded"]
    }
