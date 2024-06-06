import os
import subprocess
from datetime import datetime
import json

# Get the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set up environments
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/audit_failure_alerting_types.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/audit_failure_alerting_types.json"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip().splitlines()

# Iterate over each environment
for env_name, config in environments.items():
    # Set the AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Initialize an empty list to store JSON output
    output = []

    # AWS CLI command to get audit failure alerting types
    aws_command = [
        'aws', 'logs', 'describe-metric-filters',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the command and parse output
    command_output = run_command(aws_command)
    if command_output:
        output.extend(json.loads(command_output))

    # Determine the output file based on environment
    output_file = config[env_name + '_output_file']

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)
