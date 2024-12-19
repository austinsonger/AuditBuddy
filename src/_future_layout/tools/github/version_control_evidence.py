# github_version_control_evidence.py

"""
Generates evidence for a security audit by fetching data from a GitHub repository to demonstrate
that prior code is maintained for rollback capabilities and that version control is in use. The script uses
the GitHub API to retrieve data on branches, tags, commits, and pull requests made.
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

def get_branches():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/branches"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_tags():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/tags"
    response = requests.get(url, headers=HEADERS)
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

def filter_recent_items(items, date_key):
    recent_items = []
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_LOOK_BACK)
    for item in items:
        if datetime.strptime(item[date_key], '%Y-%m-%dT%H:%M:%SZ') > cutoff_date:
            recent_items.append(item)
    return recent_items

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    branches = get_branches()
    tags = get_tags()
    commits = get_commits()
    pull_requests = get_pull_requests()

    recent_commits = filter_recent_items(commits, 'commit.author.date')
    recent_pull_requests = filter_recent_items(pull_requests, 'closed_at')

    evidence = {
        'branches': branches,
        'tags': tags,
        'recent_commits': recent_commits,
        'recent_pull_requests': recent_pull_requests
    }

    save_to_file(evidence, 'github_version_control_evidence.json')

if __name__ == "__main__":
    main()
