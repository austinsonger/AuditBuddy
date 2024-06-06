import os
import subprocess
from datetime import datetime
import json

# Current year for output file path construction
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Environment settings for AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/configuration_evidence.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/configuration_evidence.json"
    }
}

def run_command(command):
    """Runs a given shell command using subprocess and returns the output as a list of strings."""
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    return result.stdout.splitlines()

# Iterate over each environment to execute AWS CLI commands and write outputs
for env_name, config in environments.items():
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Define the AWS CLI command to execute
    aws_command = [
        'aws', 'configservice', 'describe-configuration-recorders',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Execute the AWS CLI command
    output = run_command(aws_command)

    # Determine the output file path
    output_file = config[f'{env_name}_output_file'] if f'{env_name}_output_file' in config else None

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to the file
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("Configuration evidence collection completed.")
