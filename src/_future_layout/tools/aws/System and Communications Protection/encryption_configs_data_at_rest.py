# main.py
import sys
import os

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

"""
Description: This script collects evidence of encryption configurations for data at rest,
including backups and removable media. It does so by checking the configurations of AWS services
such as KMS, RDS, S3, EBS, and AWS Backup, and saves the evidence in a JSON file named with
the current date and environment name.
"""

def main():
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.encryption_configurations.json"

        # Define the AWS CLI commands to gather evidence of encryption configurations
        aws_commands = [
            [
                'aws', 'kms', 'list-keys',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'rds', 'describe-db-instances',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 's3api', 'list-buckets',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'ec2', 'describe-volumes',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'backup', 'list-backup-vaults',
                '--region', config.region, '--output', 'json'
            ]
        ]

        # Collect evidence for each command
        for aws_command in aws_commands:
            aws_handler.collect_evidence(command_runner, aws_command, output_file)

if __name__ == "__main__":
    main()
