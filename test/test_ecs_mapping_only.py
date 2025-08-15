import os
import tempfile
import pytest
from src.ecs_mapper import ECSMapper

@pytest.fixture
def sample_cyberark_event():
    return {
        "EventID": "12345",
        "EventType": "Logon",
        "Time": "2023-01-01T12:00:00Z",
        "SourceUserName": "admin@domain",
        "SourceIP": "192.168.1.100",
        "Safe": "Prod_Servers",
        "Reason": "Successful logon"
    }

@pytest.fixture
def ecs_mapper():
    # Create a temporary mapping file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("""field_mappings:
  - cyberark_field: "EventID"
    ecs_field: "event.id"
  - cyberark_field: "EventType"
    ecs_field: "event.action"
  - cyberark_field: "SourceUserName"
    ecs_field: "user.name"
  - cyberark_field: "SourceIP"
    ecs_field: "source.ip"
  - cyberark_field: "Safe"
    ecs_field: "cyberark.safe"
  - cyberark_field: "Reason"
    ecs_field: "message"
""")
        mapping_file = f.name
    
    yield ECSMapper(mapping_file)
    os.unlink(mapping_file)

def test_ecs_mapping_basic(sample_cyberark_event, ecs_mapper):
    result = ecs_mapper.map_to_ecs(sample_cyberark_event)
    
    assert result["event"]["id"] == "12345"
    assert result["event"]["action"] == "Logon"
    assert result["user"]["name"] == "admin@domain"
    assert result["source"]["ip"] == "192.168.1.100"
    assert result["cyberark"]["safe"] == "Prod_Servers"
    assert "Successful logon" in result["message"]
    assert "@timestamp" in result

def test_ecs_mapping_timestamp(sample_cyberark_event, ecs_mapper):
    sample_cyberark_event["Time"] = "2023-01-01T12:34:56Z"
    result = ecs_mapper.map_to_ecs(sample_cyberark_event)
    assert result["@timestamp"] == "2023-01-01T12:34:56Z"

def test_missing_fields(sample_cyberark_event, ecs_mapper):
    del sample_cyberark_event["SourceIP"]
    result = ecs_mapper.map_to_ecs(sample_cyberark_event)
    assert "source" not in result or "ip" not in result["source"]