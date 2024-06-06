import os
import subprocess
from datetime import datetime
import json

# Current year for file paths
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Setup the environments dictionary
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/configurations/{current_date}.db_audit_trail_logs.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/configurations/{current_date}.db_audit_trail_logs.json"
    }
}

def run_command(command):
    """Run the specified shell command and return the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout

# Iterate over environments
for env_name, config in environments.items():
    # Set environment variables for AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to get the database audit trail logs
    aws_command = [
        'aws', 'cloudtrail', 'lookup-events',
        '--lookup-attributes', 'AttributeKey=EventName,AttributeValue=ModifyDBInstance',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command
    output = run_command(' '.join(aws_command))

    # Determine the output file based on environment
    output_file = config[env_name[:-4] + '_output_file']

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to the specified file path
    with open(output_file, 'w') as f:
        f.write(output)

print("Database audit trail logs configurations have been fetched and saved.")
