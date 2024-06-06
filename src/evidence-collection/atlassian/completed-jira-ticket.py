import requests
import json
import os
from datetime import datetime
import schedule
import time

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Jira configuration
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

# Directory to save JSON files
OUTPUT_DIR = "/evidence-artifacts/private-sector/{current_year}/atlassian"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_completed_tickets():
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
    jql = f"project={PROJECT_KEY} AND status=Done"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, API_TOKEN)
    params = {
        "jql": jql,
        "fields": "id,key,summary,reporter,assignee,status,created,updated,resolutiondate"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        data = response.json()
        issues = data.get('issues', [])
        return issues
    else:
        print("Failed to fetch tickets")
        return []

def save_to_json(issues):
    file_name = "{current_date}-completed-tickets.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(issues, file, indent=4)
    print(f"Ticket details saved to {file_path}")

def monthly_job():
    print("Fetching completed tickets...")
    issues = fetch_completed_tickets()
    if issues:
        save_to_json(issues)

# Schedule the job every month
schedule.every().month.do(monthly_job)

# Main loop to run the scheduled tasks
print("Scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
