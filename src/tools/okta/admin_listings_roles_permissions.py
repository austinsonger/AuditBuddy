import os
import requests
import json
from datetime import datetime, timedelta

"""
This script generates evidence for a security audit from Okta.
It retrieves admin listings along with their roles and permissions for in-scope networks, only considering data from the past 365 days.

Steps:
1. Set the environment variables `OKTA_DOMAIN` and `OKTA_API_TOKEN`.
2. Ensure the Okta API token has the necessary permissions to read users, roles, and groups.
3. Run the script to generate a JSON file containing the admin listings with roles and permissions.

Functions:
- get_users(): Fetches the list of users from Okta.
- get_user_roles(user_id): Fetches roles for a given user.
- get_user_groups(user_id): Fetches groups for a given user.
- is_admin(user_roles): Checks if the user has any admin roles.
- filter_recent_users(users, days): Filters users created within the past specified number of days.
- generate_evidence(): Consolidates admin data and writes it to a JSON file.

Output:
- A JSON file named 'okta_admin_roles_permissions.json' containing the admin listings with roles and permissions for the past 365 days.

Requirements:
- Python 3.x
- requests library (install via `pip install requests`)

Author:
- Austin Songer
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

def is_admin(user_roles):
    admin_roles = ['SUPER_ADMIN', 'ORG_ADMIN', 'APP_ADMIN', 'GROUP_ADMIN']
    for role in user_roles:
        if role['type'] in admin_roles:
            return True
    return False

def filter_recent_users(users, days):
    recent_users = []
    cutoff_date = datetime.now() - timedelta(days=days)
    for user in users:
        created_date = datetime.strptime(user['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if created_date >= cutoff_date:
            recent_users.append(user)
    return recent_users

def generate_evidence():
    users = get_users()
    recent_users = filter_recent_users(users, 365)
    evidence = []

    for user in recent_users:
        user_id = user['id']
        user_roles = get_user_roles(user_id)
        if is_admin(user_roles):
            user_info = {
                'id': user_id,
                'fullName': user['profile']['firstName'] + ' ' + user['profile']['lastName'],
                'email': user['profile']['email'],
                'roles': user_roles,
                'groups': get_user_groups(user_id)
            }
            evidence.append(user_info)

    # Define file path and name
    file_path = "okta_admin_roles_permissions.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
