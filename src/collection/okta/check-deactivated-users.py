import os
import requests
from datetime import datetime

# Set your Okta domain and API token
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN')
API_TOKEN = os.getenv('API_TOKEN')

# Create the output directory if it doesn't exist
output_dir = f"lists/{datetime.now().year}/okta"
os.makedirs(output_dir, exist_ok=True)

# Set the output file path
output_file = os.path.join(output_dir, f"{datetime.now().strftime('%Y-%m-%d')}.okta-deactivated-users.json")

# Fetch the list of deactivated users
response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/users?filter=status eq \"DEPROVISIONED\"",
                        headers={"Authorization": f"SSWS {API_TOKEN}", "Accept": "application/json"})
users = response.json()

# Save the users to the output file
with open(output_file, 'w') as f:
    json.dump(users, f, indent=4)

print(f"Deactivated users have been saved to {output_file}")
