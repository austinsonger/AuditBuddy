import requests
import json
import os
from datetime import datetime, timedelta

# Atlassian (Jira) credentials
ATLASSIAN_DOMAIN = os.getenv("ATLASSIAN_DOMAIN")
ATLASSIAN_EMAIL = os.getenv("ATLASSIAN_EMAIL")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")

# Project-specific configuration
PROJECT_KEY = "CMDSD"
OUTPUT_DIR_ONBOARDING = "evidence-artifacts/personnel/onboarding/completed_tickets/"
OUTPUT_DIR_OFFBOARDING = "evidence-artifacts/personnel/offboarding/completed_tickets/"

def get_previous_month_date_range():
    # Calculate the first and last day of the previous month
    first_day_of_this_month = datetime.now().replace(day=1)
    last_day_of_previous_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    return first_day_of_previous_month.strftime('%Y-%m-%d'), last_day_of_previous_month.strftime('%Y-%m-%d')

def fetch_tickets(ticket_type):
    start_date, end_date = get_previous_month_date_range()
    url = f"https://{ATLASSIAN_DOMAIN}/rest/api/3/search"
    
    # Define JQL based on ticket type
    if ticket_type == "Onboarding":
        summary_keyword = "Onboarding Employee"
        status = "Employee Onboarded"
        output_dir = OUTPUT_DIR_ONBOARDING
    elif ticket_type == "Offboarding":
        summary_keyword = "Offboarding Employee"
        status = "Resolved"
        output_dir = OUTPUT_DIR_OFFBOARDING
    else:
        print("Invalid ticket type specified.")
        return []

    # JQL query
    jql = (f'project={PROJECT_KEY} AND summary ~ "{summary_keyword}" AND issuetype in '
           f'(Offboarding, Onboarding, "[System] Service request") AND status="{status}" '
           f'AND created >= "{start_date}" AND created <= "{end_date}"')
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN)
    params = {
        "jql": jql,
        "fields": "id,key,summary,description,reporter,assignee,status,created,updated,resolutiondate"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        data = response.json()
        issues = data.get('issues', [])
        save_to_json(issues, ticket_type, output_dir)
    else:
        print(f"Failed to fetch {ticket_type} tickets: {response.status_code}, {response.text}")

def save_to_json(issues, ticket_type, output_dir):
    if issues:
        os.makedirs(output_dir, exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d') + f"-{PROJECT_KEY}-{ticket_type.lower()}-tickets.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            json.dump(issues, file, indent=4)
        print(f"{ticket_type} tickets saved to {file_path}")
    else:
        print(f"No {ticket_type} tickets to save.")

def main():
    print(f"Fetching onboarding and offboarding tickets for project {PROJECT_KEY}...")
    fetch_tickets("Onboarding")
    fetch_tickets("Offboarding")

if __name__ == "__main__":
    main()
