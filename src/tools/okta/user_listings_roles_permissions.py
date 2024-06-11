import os
import requests
import json
from datetime import datetime

"""
It retrieves user listings along with their roles and permissions for in-scope networks.
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

def get_user_groups(user_id):
    url = f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/groups"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_evidence():
    users = get_users()
    evidence = []

    for user in users:
        user_id = user['id']
        user_info = {
            'id': user_id,
            'fullName': user['profile']['firstName'] + ' ' + user['profile']['lastName'],
            'email': user['profile']['email'],
            'roles': get_user_roles(user_id),
            'groups': get_user_groups(user_id)
        }
        evidence.append(user_info)

    # Define file path and name
    file_path = "okta_user_roles_permissions.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
