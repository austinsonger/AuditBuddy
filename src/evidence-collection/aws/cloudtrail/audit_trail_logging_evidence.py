import os
import subprocess
from datetime import datetime
import json

# Current year calculation
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Environments setup
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/configurations/{current_date}.audit_trail_logging.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/configurations/{current_date}.audit_trail_logging.json"
    }
}

# Function to run commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.splitlines()

# Main logic to process each environment
for env_name, config in environments.items():
    # Set environment variables for AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Prepare AWS CLI command
    aws_command = [
        'aws', 'cloudtrail', 'describe-trails',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Execute AWS CLI command
    output = run_command(' '.join(aws_command))
    output_json = json.dumps(output, indent=4)

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write output to file
    with open(output_file, 'w') as file:
        file.write(output_json)

    print(f"Audit trail logging evidence collected and saved to {output_file}")
