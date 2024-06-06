import os
import subprocess
from datetime import datetime
import json

# Set the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Environment configurations
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/aws_wafv2_evidence.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/aws_wafv2_evidence.json"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.splitlines()

# Process each environment
for env_name, config in environments.items():
    # Set the environment variables for AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Prepare output data
    output = []

    # AWS CLI commands to execute
    commands = [
        ['aws', 'wafv2', 'list-web-acls', '--scope', 'REGIONAL', '--region', config['region'], '--output', 'json'],
        ['aws', 'wafv2', 'list-resources-for-web-acl', '--scope', 'REGIONAL', '--region', config['region'], '--output', 'json']
    ]

    # Execute commands and collect output
    for command in commands:
        output.append(run_command(' '.join(command)))

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to a file
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("WAFv2 evidence generation complete.")
