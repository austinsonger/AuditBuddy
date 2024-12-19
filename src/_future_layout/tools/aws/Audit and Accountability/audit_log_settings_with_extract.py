# main.py
import sys
import os
from datetime import datetime, timedelta

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler


def main():
    """
    Description: This script collects evidence of audit log settings with a recent log extract
    for in-scope networks. It does so by checking the configurations of AWS CloudTrail and CloudWatch Logs,
    and saves the evidence in a JSON file named with the current date and environment name.
    """
    command_runner = CommandRunner()

    # Calculate the date 30 days ago from today for recent log extract
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.audit_log_settings.json"

        # Define the AWS CLI commands to gather evidence of audit log settings and recent logs
        aws_commands = [
            [
                'aws', 'cloudtrail', 'describe-trails',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'logs', 'describe-log-groups',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'logs', 'filter-log-events',
                '--log-group-name', '<your-log-group-name>',
                '--start-time', str(int(datetime.now().timestamp() - 30 * 86400) * 1000),
                '--end-time', str(int(datetime.now().timestamp()) * 1000),
                '--region', config.region, '--output', 'json'
            ]
        ]

        # Collect evidence for each command
        for aws_command in aws_commands:
            aws_handler.collect_evidence(command_runner, aws_command, output_file)

if __name__ == "__main__":
    main()
