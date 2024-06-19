# File: main.py

import sys
import os
from datetime import datetime, timedelta

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Calculate the start date for the last 183 days
        start_date = (datetime.now() - timedelta(days=183)).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Define the AWS CLI commands and output file paths
        commands = [
            {
                "description": "List CodeCommit repositories",
                "aws_command": ['aws', 'codecommit', 'list-repositories', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.list-repositories.json"
            },
            {
                "description": "Get CodeCommit repository commits",
                "aws_command": ['aws', 'codecommit', 'get-commit', '--repository-name', '<repository-name>', '--commit-id', '<commit-id>', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.commit-details-<repository-name>-<commit-id>.json"
            }
        ]

        # List repositories
        repositories = aws_handler.list_codecommit_repositories(command_runner)
        for repository in repositories:
            # List commits for each repository in the last 183 days
            commits = aws_handler.list_codecommit_commits(command_runner, repository, start_date)
            for commit in commits:
                commit_command = commands[1]["aws_command"].copy()
                commit_command[4] = repository  # Replace <repository-name> with actual repository name
                commit_command[6] = commit  # Replace <commit-id> with actual commit id
                output_file = commands[1]["output_file_template"].replace('<repository-name>', repository).replace('<commit-id>', commit)
                aws_handler.collect_evidence(command_runner, commit_command, output_file)

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
