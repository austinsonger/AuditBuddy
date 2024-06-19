# main.py
import sys
import os
# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    """
    Collects evidence of encryption configurations for all applicable data transfer points (i.e., VPN,
    SSH, SSL, TLS, SMTP, etc.). It does so by checking the configurations of AWS services such as VPN,
    Transfer for SFTP, ACM, and SES, and saves the evidence in a JSON file named with the current date
    and environment name.
    """
    command_runner = CommandRunner()
    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials
        aws_handler = AWSHandler(env_name, config)
        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.encryption_transfer_points.json"
        # Define the AWS CLI commands to gather evidence of encryption configurations
        aws_commands = [
            [
                'aws', 'ec2', 'describe-vpn-connections',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'transfer', 'list-servers',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'acm', 'list-certificates',
                '--region', config.region, '--output', 'json'
            ],
            [
                'aws', 'ses', 'describe-active-receipt-rule-set',
                '--region', config.region, '--output', 'json'
            ]
        ]

        # Collect evidence for each command
        for aws_command in aws_commands:
            aws_handler.collect_evidence(command_runner, aws_command, output_file)

if __name__ == "__main__":
    main()
