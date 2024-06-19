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
    This script collects evidence of all data disposals, including system disposals,
    hardware purging, document destruction, etc., during the review period (past 365 days).
    The evidence is gathered using AWS CloudTrail to look up S3 object deletion events and
    is saved in a JSON file named with the current date and environment name.
    """
    command_runner = CommandRunner()
    # Calculate the date 365 days ago from today
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials
        aws_handler = AWSHandler(env_name, config)
        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.data_disposals.json"
        # Define the AWS CLI command to get CloudTrail events related to S3 object deletions in the past 365 days
        aws_command = [
            'aws', 'cloudtrail', 'lookup-events',
            '--region', config.region,
            '--start-time', start_date,
            '--lookup-attributes', 'AttributeKey=EventName,AttributeValue=DeleteObject',
            '--output', 'json'
        ]
        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command, output_file)
if __name__ == "__main__":
    main()
