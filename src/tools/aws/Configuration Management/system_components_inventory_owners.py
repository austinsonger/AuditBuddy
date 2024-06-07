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
                "description": "List EC2 instances",
                "aws_command": ['aws', 'ec2', 'describe-instances', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-instances.json"
            },
            {
                "description": "List S3 buckets",
                "aws_command": ['aws', 's3api', 'list-buckets', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.list-s3-buckets.json"
            },
            {
                "description": "List RDS instances",
                "aws_command": ['aws', 'rds', 'describe-db-instances', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-db-instances.json"
            },
            {
                "description": "List IAM users",
                "aws_command": ['aws', 'iam', 'list-users', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.list-iam-users.json"
            },
            {
                "description": "List IAM roles",
                "aws_command": ['aws', 'iam', 'list-roles', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.list-iam-roles.json"
            }
        ]

        for command in commands:
            aws_handler.collect_evidence(command_runner, command["aws_command"], command["output_file"])

if __name__ == "__main__":
    main()

"""
NIST 800-53 Requirement ID:
- CM-8: Information System Component Inventory
- AC-2: Account Management

SOC 2 Control Number:
- CC1.2: Board of Directors and Executive Management
- CC6.2: Logical and Physical Access Controls
"""
