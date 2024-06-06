import os
import subprocess
from datetime import datetime
import json

# Define the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Setup environments dictionary with AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/key_rotation.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/key_rotation.json"
    }
}

# Function to run shell commands and capture the output
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    if result.returncode == 0:
        return result.stdout.strip().split('\n')
    else:
        raise Exception(f"Command failed: {result.stderr}")

# Iterate over each environment to set credentials and generate output
for env_name, config in environments.items():
    # Set the AWS credentials for the current environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to list keys and check their rotation status
    aws_command = [
        'aws', 'kms', 'list-keys',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command to
