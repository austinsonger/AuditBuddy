# github_change_control_records.py

"""
Fetches change control records from a GitHub repository for a sample of application code changes made. 
"""

import os
import requests
import json
from datetime import datetime, timedelta

# Constants
GITHUB_API_URL = "https://api.github.com"
DAYS_TO_LOOK_BACK = 183

# Environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')

# Headers for GitHub API
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_pull_requests():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    params = {
        'state': 'closed',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_commits():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    params = {
        'since': (datetime.utcnow() - timedelta(days=DAYS_TO_LOOK_BACK)).isoformat() + 'Z',
        'per_page': 100
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def filter_recent_pull_requests(pull_requests):
    recent_pulls = []
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_LOOK_BACK)
    for pr in pull_requests:
        if datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ') > cutoff_date:
            recent_pulls.append(pr)
    return recent_pulls

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    pull_requests = get_pull_requests()
    recent_pull_requests = filter_recent_pull_requests(pull_requests)
    commits = get_commits()

    evidence = {
        'pull_requests': recent_pull_requests,
        'commits': commits
    }

    save_to_file(evidence, 'github_change_control_records.json')

if __name__ == "__main__":
    main()

"""
NIST 800-53 Requirement ID:
- CM-3: Configuration Change Control
- CM-5: Access Restrictions for Change

SOC 2 Control Number:
- CC6.1: Logical and Physical Access Controls
- CC7.1: System Operations
"""
