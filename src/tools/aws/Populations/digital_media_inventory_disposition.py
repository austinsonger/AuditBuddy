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
    Main function to collect an inventory of digital/removable media and related disposition records.
    This includes:
    - Hard drives (EBS volumes)
    - Backup tapes (simulated by S3 objects)
    - Flash USB drives (simulated by S3 objects)
    - Removable hard drives (EBS volumes)
    - DVD/CD Blue Ray (simulated by S3 objects)

    The evidence is gathered from AWS services (S3, EBS) and saved to JSON files.
    The data is filtered to include only changes from the previous 365 days.
    """
    command_runner = CommandRunner()

    # Calculate the date 365 days ago
    start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.media_inventory.json"

        # Define the AWS CLI command for S3 objects with date filtering
        s3_inventory_command = [
            'aws', 's3api', 'list-objects-v2', '--bucket', config.app_bucket, '--region', config.region, '--query',
            f"Contents[?LastModified>='{start_date}']", '--output', 'json'
        ]

        # Define the AWS CLI command for EBS volumes with date filtering
        ebs_inventory_command = [
            'aws', 'ec2', 'describe-volumes', '--region', config.region, '--filters', f"Name=create-time,Values={start_date}", '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, s3_inventory_command, output_file)
        aws_handler.collect_evidence(command_runner, ebs_inventory_command, output_file)

if __name__ == "__main__":
    main()
