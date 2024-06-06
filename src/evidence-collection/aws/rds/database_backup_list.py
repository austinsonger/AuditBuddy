import os
import subprocess
import datetime
import json

# Current year calculation
current_year = datetime.datetime.now().year

# Setup of environment dictionaries with AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/database_backups.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/database_backups.json"
    }
}

def run_command(command):
    """Runs a shell command using subprocess and returns the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

# Iterate over each environment and perform actions
for env_name, config in environments.items():
    # Set the AWS credentials and region for the current environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to get the list of database backups
    aws_command = [
        'aws', 'rds', 'describe-db-snapshots',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Execute AWS CLI command
    output = run_command(aws_command)

    # Determine the output file path based on the environment
    output_file = config.get(f"{env_name}_output_file", "")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to the specified JSON file
    with open(output_file, 'w') as file:
        json.dump(output, file)

print("Backup evidence files have been generated for all specified environments.")
