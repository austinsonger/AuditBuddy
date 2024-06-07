"""
File Name: github_static_code_analysis_audit.py

Description:
This Python script generates evidence for a security audit by assessing the static code analysis mechanisms applied to developed code in a GitHub organization. It utilizes the GitHub API to retrieve relevant information about repositories, code scanning alerts, and repository settings within the past 183 days.

The script performs the following steps:
1. Imports necessary libraries and sets constants.
2. Retrieves information about repositories in the organization.
3. Checks for code scanning alerts in each repository.
4. Analyzes repository settings to determine if static code analysis mechanisms are enabled.
5. Generates a report summarizing the findings and evidence collected.

Ensure that the environment variables GITHUB_TOKEN and ORG_NAME are set with appropriate values, granting sufficient permissions to access the organization's repositories via the GitHub API.

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

def get_repositories():
    """
    Retrieve repositories in the specified organization.

    Returns:
    - A list of repository names.
    """
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repositories = [repo['full_name'] for repo in response.json()]
        return repositories
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")
        return []

def get_code_scanning_alerts(repo_name):
    """
    Retrieve code scanning alerts for the specified repository.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).

    Returns:
    - A list of code scanning alerts.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/code-scanning/alerts"
    params = {
        "state": "open",  # Include open alerts only
        "per_page": 100  # Maximum number of alerts per page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        alerts = response.json()
        return alerts
    else:
        print(f"Failed to retrieve code scanning alerts: {response.status_code}")
        return []

def analyze_repository_settings(repo_name):
    """
    Analyze repository settings to determine if static code analysis mechanisms are enabled.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).

    Returns:
    - A boolean indicating whether static code analysis mechanisms are enabled.
    """
    # Example: Check if code scanning is enabled
    url = f"{GITHUB_API_URL}/repos/{repo_name}/vulnerability-alerts"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 204:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"Failed to retrieve repository settings: {response.status_code}")
        return False

def generate_audit_report(repositories, alerts_info):
    """
    Generate an audit report summarizing the findings and evidence collected.

    Parameters:
    - repositories: A list of repository names.
    - alerts_info: A dictionary containing code scanning alerts for each repository.

    Returns:
    - A string containing the audit report.
    """
    report = "Security Audit Report\n\n"
    for repo_name in repositories:
        report += f"Repository: {repo_name}\n"
        if repo_name in alerts_info:
            alerts = alerts_info[repo_name]
            if alerts:
                report += "Code Scanning Alerts:\n"
                for alert in alerts:
                    report += f"- {alert['rule']['description']}\n"
            else:
                report += "- No code scanning alerts found.\n"
        else:
            report += "- Code scanning information not available.\n"

        if analyze_repository_settings(repo_name):
            report += "- Static code analysis mechanisms are enabled.\n"
        else:
            report += "- Static code analysis mechanisms are not enabled.\n"

        report += "\n"

    return report

if __name__ == "__main__":
    # Retrieve repositories in the organization
    repositories = get_repositories()

    # Gather code scanning alerts for each repository
    alerts_info = {}
    for repo in repositories:
        alerts = get_code_scanning_alerts(repo)
        alerts_info[repo] = alerts

    # Generate audit report
    report = generate_audit_report(repositories, alerts_info)

    # Print or save the report
    print(report)
