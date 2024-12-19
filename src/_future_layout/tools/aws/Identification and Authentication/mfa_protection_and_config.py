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
        
        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.mfa-enforcement.json"
        
        # Define the AWS CLI command to get IAM account summary which includes MFA information
        aws_command = [
            'aws', 'iam', 'get-account-summary', '--region', config.region, '--output', 'json'
        ]
        
        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command, output_file)
        
        # Generate another output file path for listing MFA devices
        output_file_devices = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.mfa-devices.json"
        
        # Define the AWS CLI command to list MFA devices
        aws_command_devices = [
            'aws', 'iam', 'list-mfa-devices', '--region', config.region, '--output', 'json'
        ]
        
        # Collect evidence for MFA devices
        aws_handler.collect_evidence(command_runner, aws_command_devices, output_file_devices)

if __name__ == "__main__":
    main()
