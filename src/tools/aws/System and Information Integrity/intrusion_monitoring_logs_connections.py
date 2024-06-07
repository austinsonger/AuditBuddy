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
        evidence_description = "information_system_monitoring_logs"

        # Generate the output file paths
        output_file_cloudtrail = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_cloudtrail.json"
        output_file_vpc_flow_logs = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_vpc_flow_logs.json"
        output_file_guardduty_findings = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_guardduty_findings.json"

        # Define the AWS CLI commands with output file paths
        aws_command_cloudtrail = [
            'aws', 'cloudtrail', 'lookup-events', '--region', config.region, '--output', 'json'
        ]
        aws_command_vpc_flow_logs = [
            'aws', 'ec2', 'describe-flow-logs', '--region', config.region, '--output', 'json'
        ]
        aws_command_guardduty_findings = [
            'aws', 'guardduty', 'list-findings', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_cloudtrail, output_file_cloudtrail)
        aws_handler.collect_evidence(command_runner, aws_command_vpc_flow_logs, output_file_vpc_flow_logs)
        aws_handler.collect_evidence(command_runner, aws_command_guardduty_findings, output_file_guardduty_findings)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- AU-12: Audit Generation
- SI-4: Information System Monitoring

SOC 2 Control Numbers:
- CC6.1: Security and Availability
- CC7.1: System Monitoring
"""
