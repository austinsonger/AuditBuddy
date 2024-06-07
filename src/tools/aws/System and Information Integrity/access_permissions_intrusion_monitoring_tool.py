# main.py
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

        # Define the evidence description
        evidence_description = "access_permissions_intrusion_monitoring_tool"

        # Generate the output file paths
        output_file_iam_policies = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_iam_policies.json"
        output_file_iam_roles = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_iam_roles.json"
        output_file_guardduty = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty.json"
        output_file_securityhub = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_securityhub.json"

        # Define the AWS CLI commands with output file paths
        aws_command_iam_policies = [
            'aws', 'iam', 'list-policies', '--scope', 'Local', '--region', config.region, '--output', 'json'
        ]
        aws_command_iam_roles = [
            'aws', 'iam', 'list-roles', '--region', config.region, '--output', 'json'
        ]
        aws_command_guardduty = [
            'aws', 'guardduty', 'list-detectors', '--region', config.region, '--output', 'json'
        ]
        aws_command_securityhub = [
            'aws', 'securityhub', 'describe-hub', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_iam_policies, output_file_iam_policies)
        aws_handler.collect_evidence(command_runner, aws_command_iam_roles, output_file_iam_roles)
        aws_handler.collect_evidence(command_runner, aws_command_guardduty, output_file_guardduty)
        aws_handler.collect_evidence(command_runner, aws_command_securityhub, output_file_securityhub)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- AC-2: Account Management
- AC-3: Access Enforcement
- SI-4: Information System Monitoring

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC6.6: Logical and Physical Access Controls
"""
