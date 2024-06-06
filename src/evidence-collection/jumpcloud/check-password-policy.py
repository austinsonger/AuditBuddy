import requests
import json
from datetime import datetime
import os

# Constants
API_KEY = 'your_api_key_here'  # Replace with your actual API key
URL = "https://api.jumpcloud.com/v2/policies/passwordpolicy"

def fetch_password_policy():
    """Fetch the password policy from Jumpcloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch policy: {response.status_code}")
        return {}

def write_policy_to_json(policy_data):
    """Write policy data to a JSON file with timestamp in the specified directory."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Password_Policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(policy_data, file, indent=4)
    print(f"Policy written to {file_name}")

if __name__ == "__main__":
    policy = fetch_password_policy()
    if policy:
        write_policy_to_json(policy)
