import os
import subprocess
from datetime import datetime
import json

# Set the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set up the environments dictionary
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/{current_date}.monitoring-config.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/{current_date}.monitoring-config.json"
    }
}

# Function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip().splitlines()

# Iterate over each environment and gather evidence
for env_name, config in environments.items():
    # Set AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Build the AWS CLI command
    aws_command = [
        'aws', 'cloudwatch', 'describe-alarms',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command
    output = json.loads(run_command(' '.join(aws_command)))

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the output directory exists
    os.makedirs(output_file, exist_ok=True)

    # Write the JSON output to the specified file path
    with open(f"{output_file}monitoring_config.json", "w") as file:
        json.dump(output, file, indent=4)

print("Evidence generation complete.")
