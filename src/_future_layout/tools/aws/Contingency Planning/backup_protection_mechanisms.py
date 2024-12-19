# File: main.py

import sys
import os

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

        # Define the AWS CLI commands and output file paths
        commands = [
            {
                "description": "List all S3 buckets",
                "aws_command": ['aws', 's3api', 'list-buckets', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.list-s3-buckets.json"
            },
            {
                "description": "Get bucket encryption configuration",
                "aws_command": ['aws', 's3api', 'get-bucket-encryption', '--bucket', '<bucket-name>', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.bucket-encryption-<bucket-name>.json"
            },
            {
                "description": "Describe RDS instances",
                "aws_command": ['aws', 'rds', 'describe-db-instances', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-db-instances.json"
            },
            {
                "description": "Describe RDS snapshots",
                "aws_command": ['aws', 'rds', 'describe-db-snapshots', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-db-snapshots.json"
            }
        ]

        for command in commands:
            if '<bucket-name>' in command["aws_command"]:
                buckets = aws_handler.get_s3_buckets(command_runner)
                for bucket in buckets:
                    bucket_command = command["aws_command"].copy()
                    bucket_command[4] = bucket  # Replace <bucket-name> with actual bucket name
                    output_file = command["output_file_template"].replace('<bucket-name>', bucket)
                    aws_handler.collect_evidence(command_runner, bucket_command, output_file)
            else:
                aws_handler.collect_evidence(command_runner, command["aws_command"], command["output_file"])

if __name__ == "__main__":
    main()

"""
NIST 800-53 Requirement ID:
- SC-13: Cryptographic Protection
- SI-12: Information Handling and Retention

SOC 2 Control Number:
- CC6.1: System and Information Integrity
- CC7.1: Logical and Physical Access Controls
"""
