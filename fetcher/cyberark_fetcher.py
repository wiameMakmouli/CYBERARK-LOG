import requests
from config import CYBERARK_URL, API_TOKEN

def fetch_cyberark_logs():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(CYBERARK_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching logs: {response.status_code}")
        return []
