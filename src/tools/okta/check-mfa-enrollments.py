import os
import requests
import json
from datetime import datetime

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set your Okta domain and API token
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN')
OKTA_API_TOKEN = os.getenv('OKTA_API_TOKEN')

# Create the output directory if it doesn't exist
output_dir = "/evidence-artifacts/private-sector/{current_year}/okta"
os.makedirs(output_dir, exist_ok=True)

# Set the output file path
output_file = os.path.join(output_dir, f"{current_date}.okta-mfa-enrollments.json")

# Fetch the list of users
response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/users",
                        headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
users = response.json()

# Initialize the JSON array for output
output_data = []

# Loop through each user and fetch their MFA enrollments
for user in users:
    user_id = user['id']
    username = user['profile']['login']

    factors_response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/factors",
                                    headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
    factors = factors_response.json()

    # Create a JSON object for the user with their MFA factors
    user_with_factors = {
        "id": user_id,
        "username": username,
        "factors": factors
    }
    output_data.append(user_with_factors)

# Save the MFA enrollments to the output file
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"MFA enrollments have been saved to {output_file}")
