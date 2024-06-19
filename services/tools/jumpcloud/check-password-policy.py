import requests
import json
from datetime import datetime
import os

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Constants
JUMPCLOUD_API_KEY = os.getenv('JUMPCLOUD_API_KEY')
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
    directory = f"/evidence-artifacts/{current_year}/private-sector/jumpcloud/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}{current_date}Jumpcloud_Password_Polic.json"
    with open(file_name, 'w') as file:
        json.dump(policy_data, file, indent=4)
    print(f"Policy written to {file_name}")

if __name__ == "__main__":
    policy = fetch_password_policy()
    if policy:
        write_policy_to_json(policy)
