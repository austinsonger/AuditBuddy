import os
import subprocess
from datetime import datetime
import json

# Current year calculation
current_year = datetime.datetime.now().year

# Environment setup
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/data_encryption_check.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/data_encryption_check.json"
    }
}

def run_command(command):
    """Run a shell command and return the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip().split('\n')

# Iterate over environments and perform checks
for env_name, config in environments.items():
    # Set AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to check SSL/TLS settings on ELB
    aws_command = [
        'aws', 'elbv2', 'describe-listeners',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command
    output = run_command(' '.join(aws_command))

    # Determine the output file path based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to file
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("Data encryption checks completed and results saved.")
