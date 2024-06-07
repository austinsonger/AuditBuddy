import sys
import os

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    """
    Evidence Description:
    This script collects evidence that development, production, and QA environments are separate by querying AWS resources.

    Controls:
    - NIST 800-53 Requirement ID: CM-2 (Baseline Configuration), CM-3 (Configuration Change Control), CM-4 (Security Impact Analysis)
    - SOC 2 Control Number: CC6.1 (Logical and Physical Access Controls)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for EC2 instances
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.environment_separation.json"

        # Define the AWS CLI command for describing EC2 instances with environment tag
        aws_command = [
            'aws', 'ec2', 'describe-instances', '--region', config.region, '--output', 'json',
            '--filters', f'Name=tag:Environment,Values={env_name}'
        ]

        # Collect evidence for EC2 instances
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

        # Generate the output file path for S3 buckets
        output_file_s3 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.s3_buckets_environment_separation.json"

        # Define the AWS CLI command for listing S3 buckets
        aws_command_s3 = [
            'aws', 's3api', 'list-buckets', '--query', 'Buckets[*].Name', '--output', 'json'
        ]

        # Collect evidence for S3 buckets
        s3_buckets = aws_handler.collect_evidence(command_runner, aws_command_s3, output_file_s3, return_data=True)
        for bucket in s3_buckets:
            output_file_s3_tagging = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.s3_bucket_{bucket}_tags.json"
            aws_command_s3_tagging = [
                'aws', 's3api', 'get-bucket-tagging', '--bucket', bucket, '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_s3_tagging, output_file_s3_tagging)

if __name__ == "__main__":
    main()
