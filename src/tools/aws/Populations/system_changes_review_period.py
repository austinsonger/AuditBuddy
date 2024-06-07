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
    Main function to collect evidence of all system changes made during the review period.
    This includes:
    - All in-scope application changes
    - All in-scope database changes
    - All in-scope operating system changes

    The evidence is gathered from AWS services (S3, RDS, EC2) and saved to JSON files.
    The data is filtered to include only changes from the previous 365 days.
    """
    command_runner = CommandRunner()

    # Calculate the date 365 days ago
    start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.system_changes.json"

        # Define the AWS CLI command for application changes (S3) with date filtering
        app_changes_command = [
            'aws', 's3api', 'list-object-versions', '--bucket', config.app_bucket, '--region', config.region, '--query',
            f"Versions[?LastModified>='{start_date}']", '--output', 'json'
        ]

        # Define the AWS CLI command for database changes (RDS) with date filtering
        db_changes_command = [
            'aws', 'rds', 'describe-db-instances', '--region', config.region, '--output', 'json'
        ]

        # Define the AWS CLI command for operating system changes (EC2) with date filtering
        os_changes_command = [
            'aws', 'ec2', 'describe-instances', '--region', config.region, '--filters', f"Name=launch-time,Values={start_date}", '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, app_changes_command, output_file)
        aws_handler.collect_evidence(command_runner, db_changes_command, output_file)
        aws_handler.collect_evidence(command_runner, os_changes_command, output_file)

if __name__ == "__main__":
    main()
