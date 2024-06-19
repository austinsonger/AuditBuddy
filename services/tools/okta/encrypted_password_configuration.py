import os
import requests
import json
from datetime import datetime, timedelta

"""
It retrieves configuration settings to ensure that only encrypted representations of passwords are stored and transmitted.
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

def get_password_policies():
    url = f"https://{OKTA_DOMAIN}/api/v1/policies?type=PASSWORD"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def get_security_settings():
    url = f"https://{OKTA_DOMAIN}/api/v1/org/security"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def filter_recent_policies(policies, days):
    recent_policies = []
    cutoff_date = datetime.now() - timedelta(days=days)
    for policy in policies:
        created_date = datetime.strptime(policy['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if created_date >= cutoff_date:
            recent_policies.append(policy)
    return recent_policies

def generate_evidence():
    password_policies = get_password_policies()
    security_settings = get_security_settings()

    recent_password_policies = filter_recent_policies(password_policies, 365)

    evidence = {
        'passwordPolicies': recent_password_policies,
        'securitySettings': security_settings
    }

    # Define file path and name
    file_path = "okta_encrypted_password_configuration.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
