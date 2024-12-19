import os
import requests
import json
from datetime import datetime, timedelta

"""
This script generates evidence for a security audit from Okta.
It retrieves account lockout settings for in-scope networks, only considering data from the past 365 days where applicable.

Steps:
1. Set the environment variables `OKTA_DOMAIN` and `OKTA_API_TOKEN`.
2. Ensure the Okta API token has the necessary permissions to read policies and settings.
3. Run the script to generate a JSON file containing the account lockout settings.

Functions:
- get_account_lockout_policies(): Fetches account lockout policies from Okta.
- filter_recent_policies(policies, days): Filters policies created within the past specified number of days.
- generate_evidence(): Consolidates policy data and writes it to a JSON file.

Output:
- A JSON file named 'okta_account_lockout_settings.json' containing the account lockout settings.

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

def get_account_lockout_policies():
    url = f"https://{OKTA_DOMAIN}/api/v1/policies?type=OKTA_SIGN_ON"
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
    policies = get_account_lockout_policies()
    recent_policies = filter_recent_policies(policies, 365)

    # Extract lockout settings from policies
    evidence = []
    for policy in recent_policies:
        for rule in policy.get('rules', []):
            lockout_settings = rule.get('conditions', {}).get('authContext', {}).get('authType', {})
            if lockout_settings:
                evidence.append({
                    'policyId': policy['id'],
                    'policyName': policy['name'],
                    'ruleId': rule['id'],
                    'ruleName': rule['name'],
                    'lockoutSettings': lockout_settings
                })

    # Define file path and name
    file_path = "okta_account_lockout_settings.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
