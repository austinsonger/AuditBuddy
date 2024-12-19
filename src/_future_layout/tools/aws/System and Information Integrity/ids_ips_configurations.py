# main.py
import sys
import os
"""
NIST 800-53 Control Numbers:
- SI-4: Information System Monitoring
- SI-7: Software, Firmware, and Information Integrity

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC7.1: System Monitoring
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
        evidence_description = "ids_ips_configurations"

        # Generate the output file paths
        output_file_guardduty = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty.json"
        output_file_securityhub = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_securityhub.json"
        output_file_network_firewall = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_network_firewall.json"

        # Define the AWS CLI commands with output file paths
        aws_command_guardduty = [
            'aws', 'guardduty', 'list-detectors', '--region', config.region, '--output', 'json'
        ]
        aws_command_securityhub = [
            'aws', 'securityhub', 'get-findings', '--region', config.region, '--output', 'json'
        ]
        aws_command_network_firewall = [
            'aws', 'network-firewall', 'list-firewalls', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_guardduty, output_file_guardduty)
        aws_handler.collect_evidence(command_runner, aws_command_securityhub, output_file_securityhub)
        aws_handler.collect_evidence(command_runner, aws_command_network_firewall, output_file_network_firewall)

if __name__ == "__main__":
    main()

