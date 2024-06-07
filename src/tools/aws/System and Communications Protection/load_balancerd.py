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

        # Generate the output file paths
        output_file_https = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.load_balancers_https_listeners.json"
        output_file_delete_protection = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.load_balancers_delete_protection.json"

        # Define the AWS CLI command for checking HTTPS/SSL listeners
        aws_command_https = [
            'aws', 'elbv2', 'describe-load-balancers', '--region', config.region, '--output', 'json'
        ]

        # Define the AWS CLI command for checking delete protection
        aws_command_delete_protection = [
            'aws', 'elbv2', 'describe-load-balancer-attributes', '--query', 'LoadBalancers[*].{LoadBalancerArn:LoadBalancerArn,DeletionProtectionEnabled:Attributes[?Key==`deletion_protection.enabled`].Value | [0]}', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for HTTPS/SSL listeners
        aws_handler.collect_evidence(command_runner, aws_command_https, output_file_https)

        # Collect evidence for delete protection
        aws_handler.collect_evidence(command_runner, aws_command_delete_protection, output_file_delete_protection)

if __name__ == "__main__":
    main()
