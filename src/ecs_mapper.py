import yaml
from datetime import datetime

class ECSMapper:
    def __init__(self, mapping_file):
        with open(mapping_file) as f:
            self.mappings = yaml.safe_load(f)['field_mappings']

    def map_to_ecs(self, cyberark_event):
        ecs_event = {
            "@timestamp": cyberark_event.get('Time', datetime.utcnow().isoformat()),
            "event": {
                "kind": "event",
                "category": self._determine_category(cyberark_event),
                "original": str(cyberark_event)
            }
        }

        # Apply configured field mappings
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
            return 'authentication'
        elif 'logon' in event_type:
            return 'session'
        return 'unknown'