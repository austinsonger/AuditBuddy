import os
import requests
import json
from datetime import datetime

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set your Okta domain and API token
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN')
API_TOKEN = os.getenv('API_TOKEN')

# Create the output directory if it doesn't exist
output_dir = "/evidence-artifacts/private-sector/{current_year}/okta"
os.makedirs(output_dir, exist_ok=True)

# Set the output file path
output_file = os.path.join(output_dir, f"{current_date}.okta-users-groups.json")

# Fetch the list of users
response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/users",
                        headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
users = response.json()

# Initialize the JSON array for output
output_data = []

# Loop through each user and fetch their groups
for user in users:
    user_id = user['id']
    username = user['profile']['login']

    groups_response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/groups",
                                   headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
    user_groups = groups_response.json()

    # Create a JSON object for the user with their groups
    user_with_groups = {
        "id": user_id,
        "username": username,
        "groups": user_groups
    }
    output_data.append(user_with_groups)

# Save the users and groups to the output file
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Users and their groups have been saved to {output_file}")
