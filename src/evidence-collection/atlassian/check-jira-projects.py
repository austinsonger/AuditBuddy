import os
import datetime
import requests
import json

# Set your Jira domain, email, and API token
JIRA_DOMAIN = ""
JIRA_EMAIL = ""
API_TOKEN = ""

# Create the output directory if it doesn't exist
year = datetime.datetime.now().strftime('%Y')
OUTPUT_DIR = f"lists/{year}/jira"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set the output file path
date = datetime.datetime.now().strftime('%F')
OUTPUT_FILE = f"{OUTPUT_DIR}/{date}.jira-projects.json"

# Fetch the list of projects from Jira
auth = (JIRA_EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}
response = requests.get(f"https://{JIRA_DOMAIN}/rest/api/2/project", auth=auth, headers=headers)

# Check if the API call was successful
if response.status_code != 200:
    print("Failed to fetch Jira projects")
    exit(1)

# Check if the response contains an error
data = response.json()
if 'errorMessages' in data:
    error_msg = ', '.join(data['errorMessages'])
    print(f"Error fetching Jira projects: {error_msg}")
    exit(1)

# Extract relevant fields and save to JSON file
projects = [
    {"id": project["id"], "key": project["key"], "name": project["name"], 
     "projectTypeKey": project.get("projectTypeKey", ""), 
     "lead": project.get("lead", {}).get("displayName", "")}
    for project in data
]
with open(OUTPUT_FILE, 'w') as f:
    json.dump(projects, f, indent=4)

print(f"Jira projects have been saved to {OUTPUT_FILE}")
