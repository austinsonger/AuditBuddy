import os
import requests
import json
from datetime import datetime

# Set your Okta domain and API token
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN')
API_TOKEN = os.getenv('API_TOKEN')

# Create the output directory if it doesn't exist
output_dir = f"lists/{datetime.now().year}/okta"
os.makedirs(output_dir, exist_ok=True)

# Set the output file path
output_file = os.path.join(output_dir, f"{datetime.now().strftime('%Y-%m-%d')}.okta-password-policies.json")

# Fetch the list of policies
response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/policies?type=PASSWORD",
                        headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
policies = response.json()

# Initialize the JSON array for output
output_data = []

# Loop through each policy and fetch detailed information
for policy in policies:
    policy_id = policy['id']
    policy_name = policy['name']
    policy_type = policy['type']
    policy_desc = policy.get('description', '')

    # Fetch policy rules
    rules_response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/policies/{policy_id}/rules",
                                  headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
    rules = rules_response.json()

    # Create a JSON object for the policy with its rules
    policy_with_rules = {
        "id": policy_id,
        "name": policy_name,
        "type": policy_type,
        "description": policy_desc,
        "rules": rules
    }
    output_data.append(policy_with_rules)

# Save the password policies to the output file
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Password policies have been saved to {output_file}")
