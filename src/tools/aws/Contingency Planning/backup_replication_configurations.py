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
                "description": "List all RDS instances",
                "aws_command": ['aws', 'rds', 'describe-db-instances', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-db-instances.json"
            },
            {
                "description": "Describe RDS instance read replicas",
                "aws_command": ['aws', 'rds', 'describe-db-instances', '--db-instance-identifier', '<db-instance-identifier>', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-db-replicas-<db-instance-identifier>.json"
            },
            {
                "description": "Describe S3 bucket replication configurations",
                "aws_command": ['aws', 's3api', 'get-bucket-replication', '--bucket', '<bucket-name>', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.bucket-replication-<bucket-name>.json"
            },
            {
                "description": "List EC2 AMIs",
                "aws_command": ['aws', 'ec2', 'describe-images', '--owners', 'self', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-amis.json"
            }
        ]

        for command in commands:
            if '<db-instance-identifier>' in command["aws_command"]:
                db_instances = aws_handler.get_db_instances(command_runner)
                for db_instance in db_instances:
                    db_command = command["aws_command"].copy()
                    db_command[4] = db_instance  # Replace <db-instance-identifier> with actual DB instance identifier
                    output_file = command["output_file_template"].replace('<db-instance-identifier>', db_instance)
                    aws_handler.collect_evidence(command_runner, db_command, output_file)
            elif '<bucket-name>' in command["aws_command"]:
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
- CP-6: Alternate Storage Site
- CP-9: Information System Backup

SOC 2 Control Number:
- CC6.6: Logical and Physical Access Controls
- CC7.2: System Operations
"""
