import os
import requests
import base64

# Environment variables for TriNet and JumpCloud credentials
TRINET_API_KEY = os.getenv('TRINET_API_KEY')
TRINET_API_SECRET = os.getenv('TRINET_API_SECRET')
COMPANY_ID = "CJ6"  # Replace with your actual company ID for TriNet
TRINET_TOKEN_URL = "https://api.trinet.com/oauth/accesstoken?grant_type=client_credentials"

JUMPCLOUD_API_KEY = os.getenv('JUMPCLOUD_API_KEY')
JUMPCLOUD_BASE_URL = 'https://api.jumpcloud.com'

# Headers for JumpCloud API
jumpcloud_headers = {
    'x-api-key': JUMPCLOUD_API_KEY,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Define attribute mappings between TriNet and JumpCloud
ATTRIBUTE_MAP = {
    'jobTitle': 'jobTitle',
    'department': 'department',
    'location': 'location',
}

# Helper function to get access token for TriNet
def get_trinet_access_token(api_key, api_secret):
    client_credentials = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }
    response = requests.get(TRINET_TOKEN_URL, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        raise Exception(f"Error getting access token: {response.text}")

# Fetch TriNet access token
TRINET_ACCESS_TOKEN = get_trinet_access_token(TRINET_API_KEY, TRINET_API_SECRET)

# Headers for TriNet API requests (with dynamic access token)
def get_trinet_headers():
    return {
        'Authorization': f'Bearer {TRINET_ACCESS_TOKEN}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

# Function to fetch all users from TriNet
def get_trinet_users():
    url = f"https://api.trinet.com/v1/companies/{COMPANY_ID}/employees"
    headers = get_trinet_headers()
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['employees']
    else:
        print("Error fetching users from TriNet:", response.status_code, response.text)
        return []

# Function to fetch a user from JumpCloud by email
def get_jumpcloud_user(email):
    url = f"{JUMPCLOUD_BASE_URL}/api/systemusers?filter=email:eq:{email}"
    response = requests.get(url, headers=jumpcloud_headers)
    
    if response.status_code == 200 and response.json()['results']:
        return response.json()['results'][0]
    else:
        print(f"JumpCloud user not found for email: {email}")
        return None

# Function to update user attributes in JumpCloud
def update_jumpcloud_user(user_id, updated_attributes):
    url = f"{JUMPCLOUD_BASE_URL}/api/systemusers/{user_id}"
    response = requests.put(url, headers=jumpcloud_headers, json=updated_attributes)
    
    if response.status_code == 200:
        print(f"Successfully updated JumpCloud user ID: {user_id}")
    else:
        print(f"Failed to update JumpCloud user ID: {user_id}", response.status_code, response.text)

# Function to sync attributes from TriNet to JumpCloud
def sync_attributes():
    trinet_users = get_trinet_users()
    
    for trinet_user in trinet_users:
        email = trinet_user['workEmail']
        jumpcloud_user = get_jumpcloud_user(email)
        
        if jumpcloud_user:
            # Prepare the updated attributes for JumpCloud
            updated_attributes = {}
            for trinet_attr, jumpcloud_attr in ATTRIBUTE_MAP.items():
                trinet_value = trinet_user.get(trinet_attr)
                jumpcloud_value = jumpcloud_user.get(jumpcloud_attr)
                
                # If the attribute exists and differs, add to update payload
                if trinet_value and trinet_value != jumpcloud_value:
                    updated_attributes[jumpcloud_attr] = trinet_value
            
            # Update user in JumpCloud if there are changes
            if updated_attributes:
                update_jumpcloud_user(jumpcloud_user['_id'], updated_attributes)

# Run the synchronization process
sync_attributes()
