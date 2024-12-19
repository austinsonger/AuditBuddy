import os
import requests
import json
from datetime import datetime, timedelta

"""
It retrieves audit logs from the centralized auditing mechanism for each of the defined auditable events in AU-2.a.1, considering data from the past 365 days.
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

def get_audit_logs():
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

def generate_evidence():
    logs = get_audit_logs()
    recent_logs = filter_recent_logs(logs, 365)

    evidence = []
    for log in recent_logs:
        event_info = {
            'eventType': log.get('eventType'),
            'eventTime': log.get('published'),
            'eventLocation': log.get('client', {}).get('geographicalContext', {}).get('geolocation', {}),
            'eventSource': log.get('client', {}).get('ipAddress'),
            'eventOutcome': log.get('outcome', {}).get('result'),
            'eventActor': log.get('actor', {}).get('id')
        }
        evidence.append(event_info)

    # Define file path and name
    file_path = "okta_audit_logs.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
