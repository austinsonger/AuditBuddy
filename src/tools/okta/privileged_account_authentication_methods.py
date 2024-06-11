import os
import requests
import json
from datetime import datetime, timedelta

"""
It retrieves authentication methods used to access privileged accounts for in-scope networks.
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

def get_users():
    url = f"https://{OKTA_DOMAIN}/api/v1/users"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def get_user_roles(user_id):
    url = f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/roles"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def is_privileged_account(user_roles):
    privileged_roles = ['SUPER_ADMIN', 'ORG_ADMIN', 'APP_ADMIN', 'GROUP_ADMIN']
    for role in user_roles:
        if role['type'] in privileged_roles:
            return True
    return False

def get_authentication_methods(user_id):
    url = f"https://{OKTA_DOMAIN}/api/v1/logs?filter=actor.id+eq+\"{user_id}\"+and+eventType+eq+\"user.authentication.auth_via_mfa\""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def filter_recent_events(events, days):
    recent_events = []
    cutoff_date = datetime.now() - timedelta(days=days)
    for event in events:
        event_date = datetime.strptime(event['published'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if event_date >= cutoff_date:
            recent_events.append(event)
    return recent_events

def generate_evidence():
    users = get_users()
    evidence = []

    for user in users:
        user_id = user['id']
        user_roles = get_user_roles(user_id)
        if is_privileged_account(user_roles):
            auth_methods = get_authentication_methods(user_id)
            recent_auth_methods = filter_recent_events(auth_methods, 365)
            for method in recent_auth_methods:
                evidence.append({
                    'userId': user_id,
                    'userName': user['profile']['login'],
                    'authMethod': method['authenticationContext']['authenticationStep'],
                    'timestamp': method['published']
                })

    # Define file path and name
    file_path = "okta_privileged_account_authentication_methods.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
