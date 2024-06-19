import os
import requests
import json
from datetime import datetime, timedelta

"""
It retrieves access control settings for log files, considering data from the past 365 days.
"""

# Set environment variables for Okta domain and API token
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN')
OKTA_API_TOKEN = os.getenv('OKTA_API_TOKEN')

# Define headers for API requests
headers = {
    'Authorization': f'SSWS {OKTA_API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def get_system_log():
    url = f"https://{OKTA_DOMAIN}/api/v1/logs"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def filter_recent_logs(logs, days):
    recent_logs = []
    cutoff_date = datetime.now() - timedelta(days=days)
    for log in logs:
        event_date = datetime.strptime(log['published'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if event_date >= cutoff_date:
            recent_logs.append(log)
    return recent_logs

def extract_access_control_info(logs):
    access_control_info = []
    for log in logs:
        if log['eventType'] == 'system.access_control':
            access_control_info.append({
                'eventId': log['uuid'],
                'eventType': log['eventType'],
                'timestamp': log['published'],
                'actor': log['actor'],
                'target': log['target'],
                'outcome': log['outcome'],
                'accessControl': log['debugContext']['debugData']
            })
    return access_control_info

def generate_evidence():
    logs = get_system_log()
    recent_logs = filter_recent_logs(logs, 365)
    access_control_info = extract_access_control_info(recent_logs)

    # Define file path and name
    file_path = "okta_access_control_log_files.json"
    with open(file_path, 'w') as f:
        json.dump(access_control_info, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
