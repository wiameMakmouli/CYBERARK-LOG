import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

@pytest.fixture
def mock_config():
    return {
        "cyberark": {
            "pvwa_url": "http://localhost",
            "api_path": "/PasswordVault/api",
            "username": "test",
            "password": "test",
            "verify_ssl": False
        },
        "logstash": {
            "host": "localhost",
            "port": 5044,
            "use_ssl": False
        },
        "settings": {
            "polling_interval": 1,
            "initial_lookback_hours": 1,
            "max_events_per_poll": 100
        }
    }

def test_full_flow(mock_config):
    # Mock the entire pipeline
    with patch("src.cyberark_client.CyberArkClient") as MockClient, \
         patch("src.ecs_mapper.ECSMapper") as MockMapper, \
         patch("src.logstash_sender.LogstashSender") as MockSender:
        
        # Setup mock returns
        mock_client = MockClient.return_value
        mock_client.get_security_events.return_value = [{
            "EventID": "123",
            "EventType": "Logon",
            "Time": "2023-01-01T00:00:00Z"
        }]

        mock_mapper = MockMapper.return_value
        mock_mapper.map_to_ecs.return_value = {
            "event": {"id": "123", "action": "Logon"},
            "@timestamp": "2023-01-01T00:00:00Z"
        }

        mock_sender = MockSender.return_value
        mock_sender.send.return_value = True

        # Import and run main() AFTER patching
        from src.main import main
        main()  # Should exit after one iteration due to mock polling

        # Verify calls
        mock_client.get_security_events.assert_called_once()
        mock_mapper.map_to_ecs.assert_called_once_with({
            "EventID": "123",
            "EventType": "Logon",
            "Time": "2023-01-01T00:00:00Z"
        })
        mock_sender.send.assert_called_once_with({
            "event": {"id": "123", "action": "Logon"},
            "@timestamp": "2023-01-01T00:00:00Z"
        })