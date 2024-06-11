# main.py
import sys
import os
"""
NIST 800-53 Control Numbers:
- CA-7: Continuous Monitoring
- SI-4: Information System Monitoring

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC7.2: Change Management
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
        evidence_description = "sharing_intrusion_monitoring_information"

        # Generate the output file paths
        output_file_guardduty_members = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty_members.json"
        output_file_securityhub_members = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_securityhub_members.json"
        output_file_securityhub_standards = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_securityhub_standards.json"

        # Define the AWS CLI commands with output file paths
        aws_command_guardduty_members = [
            'aws', 'guardduty', 'list-members', '--region', config.region, '--output', 'json'
        ]
        aws_command_securityhub_members = [
            'aws', 'securityhub', 'list-members', '--region', config.region, '--output', 'json'
        ]
        aws_command_securityhub_standards = [
            'aws', 'securityhub', 'describe-standards-subscriptions', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_guardduty_members, output_file_guardduty_members)
        aws_handler.collect_evidence(command_runner, aws_command_securityhub_members, output_file_securityhub_members)
        aws_handler.collect_evidence(command_runner, aws_command_securityhub_standards, output_file_securityhub_standards)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- CA-7: Continuous Monitoring
- SI-4: Information System Monitoring

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC7.2: Change Management
"""
