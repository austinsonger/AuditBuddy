import os
import subprocess
from datetime import datetime
import json

def run_command(command):
    """
    Run a shell command using subprocess.run and return the command output as a list of strings.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.splitlines()

# Define the current year and date
current_year = datetime.now().year

# Set up environments dictionary
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/"
    }
}

# AWS CLI command to retrieve encryption configuration for databases
aws_cli_command = "aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier, StorageEncrypted]' --output json"

# Iterate over each environment
for env_name, config in environments.items():
    # Set AWS credentials
    os.environ["AWS_ACCESS_KEY_ID"] = config['access_key']
    os.environ["AWS_SECRET_ACCESS_KEY"] = config['secret_key']
    os.environ["AWS_DEFAULT_REGION"] = config['region']
    
    # Initialize empty list for JSON output
    output = run_command(aws_cli_command)
    
    # Determine the output file path
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']
    
    # Ensure output directory exists
    os.makedirs(output_file, exist_ok=True)
    
    # Write JSON output to file
    with open(os.path.join(output_file, 'encryption_config.json'), 'w') as f:
        json.dump(output, f, indent=4)

