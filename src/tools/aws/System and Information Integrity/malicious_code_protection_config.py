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
        evidence_description = "malicious_code_protection_configuration"

        # Generate the output file paths
        output_file_guardduty_detectors = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty_detectors.json"
        output_file_guardduty_threats = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty_threats.json"
        output_file_securityhub_findings = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_securityhub_findings.json"

        # Define the AWS CLI commands with output file paths
        aws_command_guardduty_detectors = [
            'aws', 'guardduty', 'list-detectors', '--region', config.region, '--output', 'json'
        ]
        aws_command_guardduty_threats = [
            'aws', 'guardduty', 'list-findings', '--region', config.region, '--output', 'json'
        ]
        aws_command_securityhub_findings = [
            'aws', 'securityhub', 'get-findings', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_guardduty_detectors, output_file_guardduty_detectors)
        aws_handler.collect_evidence(command_runner, aws_command_guardduty_threats, output_file_guardduty_threats)
        aws_handler.collect_evidence(command_runner, aws_command_securityhub_findings, output_file_securityhub_findings)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- SI-3: Malicious Code Protection
- SI-4: Information System Monitoring

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC7.1: System Monitoring
"""
