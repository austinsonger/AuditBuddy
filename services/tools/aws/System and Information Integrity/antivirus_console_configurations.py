# main.py
import sys
import os

"""
NIST 800-53 Control Numbers:
- MP-7: Media Use
- MP-8: Media Downgrading

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC6.8: Confidentiality and Processing Integrity
"""
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

        # Define the evidence description
        evidence_description = "removable_media_configurations"

        # Generate the output file paths
        output_file_ec2 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_ec2.json"
        output_file_s3 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_s3.json"
        output_file_ebs = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_ebs.json"

        # Define the AWS CLI commands with output file paths
        aws_command_ec2 = [
            'aws', 'ec2', 'describe-instances', '--region', config.region, '--output', 'json'
        ]
        aws_command_s3 = [
            'aws', 's3api', 'list-buckets', '--region', config.region, '--output', 'json'
        ]
        aws_command_ebs = [
            'aws', 'ec2', 'describe-volumes', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_ec2, output_file_ec2)
        aws_handler.collect_evidence(command_runner, aws_command_s3, output_file_s3)
        aws_handler.collect_evidence(command_runner, aws_command_ebs, output_file_ebs)

if __name__ == "__main__":
    main()
