# github_audit_logs_evidence.py

"""
The script aims to capture details of each auditable event as defined in AU-2.a.1, including:
- Type of event
- When the event occurred
- Where the event occurred
- Source of the event
- Outcome of the event
- Identity of individuals or subjects associated with the event
"""

import os
import requests
import json
from datetime import datetime, timedelta

# Constants
GITHUB_API_URL = "https://api.github.com"
DAYS_TO_LOOK_BACK = 183

# Environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_NAME = os.getenv('ORG_NAME')

# Headers for GitHub API
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_audit_logs():
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/audit-log"
    params = {
        'per_page': 100,
        'include': 'all'
    }
    all_logs = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        logs = response.json()
        all_logs.extend(logs)
        url = response.links.get('next', {}).get('url')
    return all_logs

def filter_recent_logs(logs):
    recent_logs = []
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_LOOK_BACK)
    for log in logs:
        event_time = datetime.strptime(log['@timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if event_time > cutoff_date:
            recent_logs.append(log)
    return recent_logs

def format_audit_log(log):
    return {
        'event_type': log.get('action'),
        'event_time': log.get('@timestamp'),
        'event_location': log.get('repository', log.get('org', {})).get('name'),
        'event_source': log.get('actor', {}).get('login'),
        'event_outcome': log.get('action'),
        'associated_identity': log.get('actor', {}).get('login')
    }

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    audit_logs = get_audit_logs()
    recent_audit_logs = filter_recent_logs(audit_logs)
    formatted_logs = [format_audit_log(log) for log in recent_audit_logs]

    save_to_file(formatted_logs, 'github_audit_logs_evidence.json')

if __name__ == "__main__":
    main()
