import yaml
from datetime import datetime

class ECSMapper:
    def __init__(self, mapping_file):
        with open(mapping_file) as f:
            self.mappings = yaml.safe_load(f)['field_mappings']

    def map_to_ecs(self, cyberark_event):
        ecs_event = {
            "@timestamp": cyberark_event.get('Time', datetime.utcnow().isoformat()),

            # Agent (Elastic Agent/Filebeat info – statique ou configurable)
            "agent": {
                "ephemeral_id": "generated-ephemeral-id",
                "id": "generated-agent-id",
                "name": "cyberark-collector",
                "type": "custom-script",
                "version": "1.0.0"
            },

            # Bloc cyberarkpas.audit
            "cyberarkpas": {
                "audit": {
                    "action": cyberark_event.get("Action", ""),
                    "desc": cyberark_event.get("Description", ""),
                    "iso_timestamp": cyberark_event.get("Time", datetime.utcnow().isoformat()),
                    "issuer": cyberark_event.get("UserName", ""),
                    "message": cyberark_event.get("Message", ""),
                    "rfc5424": True,
                    "severity": cyberark_event.get("Severity", "Info"),
                    "station": cyberark_event.get("SourceMachine", ""),
                    "timestamp": cyberark_event.get("Time", "")
                }
            },

            # Dataset (statique)
            "data_stream": {
                "dataset": "cyberarkpas.audit",
                "namespace": "default",
                "type": "logs"
            },

            "ecs": {
                "version": "8.11.0"
            },

            "event": {
                "action": self._determine_action(cyberark_event),
                "category": self._determine_category(cyberark_event),
                "dataset": "cyberarkpas.audit",
                "kind": "event",
                "outcome": self._determine_outcome(cyberark_event),
                "severity": self._map_severity(cyberark_event.get("Severity", "")),
                "type": ["start"]
            },

            "host": {
                "name": cyberark_event.get("Component", "VAULT")
            },

            "observer": {
                "hostname": cyberark_event.get("Component", "VAULT"),
                "product": "Vault",
                "vendor": "Cyber-Ark",
                "version": cyberark_event.get("Version", "unknown")
            },

            "related": {
                "ip": [cyberark_event.get("SourceMachine", "")],
                "user": [cyberark_event.get("UserName", "")]
            },

            "source": {
                "ip": cyberark_event.get("SourceMachine", "")
            },

            "user": {
                "name": cyberark_event.get("UserName", "")
            },

            "tags": ["cyberarkpas-audit", "forwarded"]
        }

        # Application des mappings configurés
        for mapping in self.mappings:
            if mapping['cyberark_field'] in cyberark_event:
                self._set_nested_field(
                    ecs_event,
                    mapping['ecs_field'],
                    cyberark_event[mapping['cyberark_field']]
                )

        return ecs_event

    def _set_nested_field(self, obj, field_path, value):
        keys = field_path.split('.')
        for key in keys[:-1]:
            obj = obj.setdefault(key, {})
        obj[keys[-1]] = value

    def _determine_category(self, event):
        event_type = event.get('EventType', '').lower()
        if 'password' in event_type:
            return ["authentication"]
        elif 'logon' in event_type:
            return ["authentication", "session"]
        return ["unknown"]

    def _determine_action(self, event):
        action = event.get("Action", "").lower()
        if "logon" in action and event.get("Result", "").lower() == "success":
            return "authentication_success"
        elif "logon" in action:
            return "authentication_failure"
        return action or "unknown"

    def _determine_outcome(self, event):
        result = event.get("Result", "").lower()
        if "success" in result:
            return "success"
        elif "fail" in result:
            return "failure"
        return "unknown"

    def _map_severity(self, severity):
        mapping = {
            "info": 2,
            "warning": 4,
            "error": 6,
            "critical": 9
        }
        return mapping.get(severity.lower(), 1)
