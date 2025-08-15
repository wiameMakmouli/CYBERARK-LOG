import requests
from datetime import datetime, timedelta
import logging

class CyberArkClient:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.verify = self.config['cyberark']['verify_ssl']
        self.token = None
        self.last_event_time = datetime.utcnow() - timedelta(
            hours=self.config['settings']['initial_lookback_hours'])

    def authenticate(self):
        auth_url = f"{self.config['cyberark']['pvwa_url']}{self.config['cyberark']['api_path']}/auth/LDAP/Logon"
        try:
            response = self.session.post(
                auth_url,
                json={
                    "Username": self.config['cyberark']['username'],
                    "Password": self.config['cyberark']['password']
                }
            )
            response.raise_for_status()
            self.token = response.json()['CyberArkLogonResult']
            return True
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False

    def get_security_events(self):
        if not self.token and not self.authenticate():
            return []

        events_url = f"{self.config['cyberark']['pvwa_url']}{self.config['cyberark']['api_path']}/Events"
        
        params = {
            "fromDate": self.last_event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "toDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit": self.config['settings']['max_events_per_poll']
        }

        try:
            response = self.session.get(
                events_url,
                headers={"Authorization": self.token},
                params=params
            )
            response.raise_for_status()
            events = response.json().get('Events', [])
            
            if events:
                self.last_event_time = datetime.strptime(
                    events[-1]['Time'], "%Y-%m-%dT%H:%M:%SZ")
                
            return events
        except Exception as e:
            self.logger.error(f"Failed to fetch events: {str(e)}")
            return []