import os
import requests
import json
from datetime import datetime, timedelta

"""
It retrieves the configuration settings to disable identifiers after a defined period of 
account inactivity, considering data from the past 365 days where applicable.
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

def get_inactivity_policies():
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
    policies = get_inactivity_policies()
    recent_policies = filter_recent_policies(policies, 365)

    evidence = []
    for policy in recent_policies:
        for rule in policy.get('rules', []):
            actions = rule.get('actions', {}).get('signon', {}).get('actions', {})
            if 'disable' in actions:
                evidence.append({
                    'policyId': policy['id'],
                    'policyName': policy['name'],
                    'ruleId': rule['id'],
                    'ruleName': rule['name'],
                    'disableAfterInactivity': actions['disable']
                })

    # Define file path and name
    file_path = "okta_inactivity_account_disabling_config.json"
    with open(file_path, 'w') as f:
        json.dump(evidence, f, indent=4)

    print(f"Evidence has been written to {file_path}")

if __name__ == "__main__":
    generate_evidence()
