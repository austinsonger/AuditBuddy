"""
Generates evidence for a security audit by assessing the integrity verification mechanisms for software and 
firmware components in a GitHub organization. It utilizes the GitHub API to retrieve relevant information about 
commits, pull requests, and repository settings.
"""

import os
import requests
from datetime import datetime, timedelta

# Constants
GITHUB_API_URL = "https://api.github.com"
DAYS_TO_LOOK_BACK = 183

# Environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_NAME = os.getenv('ORG_NAME')

# Headers for GitHub API
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_commits(repo_name, since_date):
    """
    Retrieve commits made to the specified repository since the given date.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).
    - since_date: The date from which to retrieve commits (ISO 8601 format).

    Returns:
    - A list of commit messages.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/commits"
    params = {
        "since": since_date,
        "per_page": 100  # Maximum number of commits per page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        commits = [commit['commit']['message'] for commit in response.json()]
        return commits
    else:
        print(f"Failed to retrieve commits: {response.status_code}")
        return []

def get_pull_requests(repo_name, since_date):
    """
    Retrieve pull requests made to the specified repository since the given date.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).
    - since_date: The date from which to retrieve pull requests (ISO 8601 format).

    Returns:
    - A list of pull request titles and descriptions.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/pulls"
    params = {
        "state": "all",  # Include closed pull requests
        "since": since_date,
        "per_page": 100  # Maximum number of pull requests per page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        pull_requests = [(pr['title'], pr['body']) for pr in response.json()]
        return pull_requests
    else:
        print(f"Failed to retrieve pull requests: {response.status_code}")
        return []

def get_repository_settings(repo_name):
    """
    Retrieve settings of the specified repository.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).

    Returns:
    - A dictionary containing repository settings.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/branches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        settings = response.json()
        return settings
    else:
        print(f"Failed to retrieve repository settings: {response.status_code}")
        return {}

def analyze_commits_pull_requests(commits, pull_requests):
    """
    Analyze commit messages and pull request descriptions to identify evidence of integrity verification mechanisms.

    Parameters:
    - commits: A list of commit messages.
    - pull_requests: A list of pull request titles and descriptions.

    Returns:
    - A list of identified integrity verification mechanisms.
    """
    # Add any keywords or patterns related to integrity verification mechanisms
    keywords = ["integrity verification", "checksum", "hash", "signature"]

    evidence = []

    # Search commits for keywords
    for commit in commits:
        for keyword in keywords:
            if keyword in commit.lower():
                evidence.append(f"Commit: {commit}")
                break  # Move to the next commit

    # Search pull request titles and descriptions for keywords
    for title, description in pull_requests:
        for keyword in keywords:
            if keyword in title.lower() or keyword in description.lower():
                evidence.append(f"Pull Request: {title} - {description}")
                break  # Move to the next pull request

    return evidence

def analyze_repository_settings(settings):
    """
    Analyze repository settings to identify enabled integrity verification features.

    Parameters:
    - settings: A dictionary containing repository settings.

    Returns:
    - A list of identified integrity verification features.
    """
    features = []

    # Example: Check if branch protection rules are enabled
    for branch in settings:
        if branch.get("protected"):
            features.append(f"Branch protection enabled for {branch['name']}")

    return features

def generate_audit_report(evidence, features):
    """
    Generate an audit report summarizing the findings and evidence collected.

    Parameters:
    - evidence: A list of identified evidence related to integrity verification mechanisms.
    - features: A list of identified integrity verification features.

    Returns:
    - A string containing the audit report.
    """
    report = "Security Audit Report\n\n"
    report += "Evidence of Integrity Verification Mechanisms:\n"
    if evidence:
        for item in evidence:
            report += f"- {item}\n"
    else:
        report += "- No evidence found.\n"

    report += "\nEnabled Integrity Verification Features:\n"
    if features:
        for feature in features:
            report += f"- {feature}\n"
    else:
        report += "- No features found.\n"

    return report

if __name__ == "__main__":
    # Retrieve repositories in the organization
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repositories = [repo['full_name'] for repo in response.json()]
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")
        repositories = []

    # Gather evidence for each repository
    all_evidence = []
    for repo in repositories:
        commits = get_commits(repo, (datetime.now() - timedelta(days=DAYS_TO_LOOK_BACK)).isoformat())
        pull_requests = get_pull_requests(repo, (datetime.now() - timedelta(days=DAYS_TO_LOOK_BACK)).isoformat())
        evidence = analyze_commits_pull_requests(commits, pull_requests)
        all_evidence.extend(evidence)

    # Analyze repository settings for each repository
    all_features = []
    for repo in repositories:
        settings = get_repository_settings(repo)
        features = analyze_repository_settings(settings)
        all_features.extend(features)

    # Generate audit report
    report = generate_audit_report(all_evidence, all_features)

    # Print or save the report
    print(report)
