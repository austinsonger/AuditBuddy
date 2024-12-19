import requests
import json
import os
from datetime import datetime

# Jira credentials
ATLASSIAN_DOMAIN = os.getenv("ATLASSIAN_DOMAIN")
ATLASSIAN_EMAIL = os.getenv("ATLASSIAN_EMAIL")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")

# Directory paths and project keys
PROJECTS = {
    "CORP_DEV": {
        "project_keys": ["PLAT", "MB"],  
        "output_dir": "evidence-artifacts/commercial/atlassian/completed_tickets/corp-dev/"
    },
    "CORP_DEVOPS": {
        "project_keys": ["CMD", "DW"],  
        "output_dir": "evidence-artifacts/commercial/atlassian/completed_tickets/corp-devops/"
    },
    "FED_DEV": {
        "project_keys": ["HB"],  
        "output_dir": "evidence-artifacts/federal/atlassian/completed_tickets/fed-dev/"
    },
    "FED_DEVOPS": {
        "project_keys": ["CAB"],  
        "output_dir": "evidence-artifacts/federal/atlassian/completed_tickets/fed-devops/"
    }
}

def fetch_completed_tickets(project_key):
    url = f"https://{ATLASSIAN_DOMAIN}/rest/api/3/search"
    jql = f"project={project_key} AND status=Done"
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
        return issues
    else:
        print(f"Failed to fetch tickets for project {project_key}: {response.status_code}, {response.text}")
        return []

def save_to_json(project_key, output_dir, issues):
    if issues:
        os.makedirs(output_dir, exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d') + f"-{project_key}-completed-tickets.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            json.dump(issues, file, indent=4)
        print(f"Ticket details for {project_key} saved to {file_path}")
    else:
        print(f"No completed tickets to save for project {project_key}.")

def main():
    for project_name, project_info in PROJECTS.items():
        project_key = project_info["project_key"]
        output_dir = project_info["output_dir"]
        
        print(f"Fetching completed tickets for project {project_key}...")
        issues = fetch_completed_tickets(project_key)
        save_to_json(project_key, output_dir, issues)

if __name__ == "__main__":
    main()
