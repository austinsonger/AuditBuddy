"""
File Name: github_dynamic_code_analysis_audit.py

Description:
This Python script generates evidence for a security audit by assessing the dynamic code analysis mechanisms applied to developed code, specifically focusing on OWASP ZAP (Zed Attack Proxy), in a GitHub organization. It utilizes the GitHub API to retrieve relevant information about repositories, workflow runs, and workflow job logs within the past 183 days.

The script performs the following steps:
1. Imports necessary libraries and sets constants.
2. Retrieves information about repositories in the organization.
3. Checks for workflow runs associated with OWASP ZAP dynamic code analysis.
4. Retrieves logs for each workflow job run to analyze OWASP ZAP scan results.
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

def get_workflow_runs(repo_name):
    """
    Retrieve workflow runs for the specified repository.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).

    Returns:
    - A list of workflow runs.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/actions/runs"
    params = {
        "workflow_id": "YOUR_WORKFLOW_ID",  # Replace with the actual workflow ID
        "event": "push",
        "per_page": 100  # Maximum number of runs per page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        runs = response.json()['workflow_runs']
        return runs
    else:
        print(f"Failed to retrieve workflow runs: {response.status_code}")
        return []

def get_workflow_job_logs(repo_name, run_id):
    """
    Retrieve logs for the specified workflow job run in the repository.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).
    - run_id: The ID of the workflow run.

    Returns:
    - A string containing the logs.
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/actions/runs/{run_id}/logs"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logs = response.json()['content']
        return logs
    else:
        print(f"Failed to retrieve workflow job logs: {response.status_code}")
        return ""

def analyze_workflow_runs(repositories):
    """
    Analyze workflow runs to identify evidence of OWASP ZAP dynamic code analysis.

    Parameters:
    - repositories: A list of repository names.

    Returns:
    - A list of identified workflow runs.
    """
    # Example: Check if workflow runs are associated with OWASP ZAP
    identified_runs = []

    for repo in repositories:
        runs = get_workflow_runs(repo)
        for run in runs:
            # Example: Check workflow run name or other metadata for OWASP ZAP
            if "OWASP ZAP" in run['name'] or "zap" in run['name'].lower():
                identified_runs.append((repo, run))

    return identified_runs

def analyze_workflow_job_logs(repo_name, identified_runs):
    """
    Analyze workflow job logs to extract OWASP ZAP scan results.

    Parameters:
    - repo_name: The name of the repository (format: owner/repository).
    - identified_runs: A list of identified workflow runs.

    Returns:
    - A dictionary containing OWASP ZAP scan results for each identified run.
    """
    # Example: Extract OWASP ZAP scan results from job logs
    zap_scan_results = {}

    for repo, run in identified_runs:
        logs = get_workflow_job_logs(repo, run['id'])
        # Example: Parse logs to find OWASP ZAP scan results
        # Example logic: if "OWASP ZAP scan complete" in logs:
        #                   zap_scan_results[repo] = "OWASP ZAP scan passed"
        #                else:
        #                   zap_scan_results[repo] = "OWASP ZAP scan failed"
        zap_scan_results[repo] = logs

    return zap_scan_results

def generate_audit_report(identified_runs, zap_scan_results):
    """
    Generate an audit report summarizing the findings and evidence collected.

    Parameters:
    - identified_runs: A list of identified workflow runs.
    - zap_scan_results: A dictionary containing OWASP ZAP scan results for each identified run.

    Returns:
    - A string containing the audit report.
    """
    report = "Security Audit Report\n\n"
    for repo, run in identified_runs:
        report += f"Repository: {repo}\n"
        report += f"Workflow Run: {run['name']}\n"
        if repo in zap_scan_results:
            report += "OWASP ZAP Scan Results:\n"
            report += zap_scan_results[repo]
        else:
            report += "- OWASP ZAP scan results not available.\n"
        report += "\n"

    return report

if __name__ == "__main__":
    # Retrieve repositories in the organization
    repositories = get_repositories()

    # Analyze workflow runs to identify OWASP ZAP scans
    identified_runs = analyze_workflow_runs(repositories)

    # Analyze workflow job logs for OWASP ZAP scan results
    zap_scan_results = analyze_workflow_job_logs(repositories, identified_runs)

    # Generate audit report
    report = generate_audit_report(identified_runs, zap_scan_results)

    # Print or save the report
    print(report)
