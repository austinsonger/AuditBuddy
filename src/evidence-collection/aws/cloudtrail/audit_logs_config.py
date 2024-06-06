import os
import subprocess
import datetime
import json

# Current date and 365 days ago calculations
current_date = datetime.datetime.now()
start_date = current_date - datetime.timedelta(days=365)

# Environments setup with AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_date.year}/private-sector/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_date.year}/federal/"
    }
}

def run_command(command):
    """ Execute the provided shell command and return the output as a list of strings. """
    process = subprocess.run(command, text=True, capture_output=True, shell=True)
    return process.stdout.splitlines()

# Main processing loop for each environment
for env_name, config in environments.items():
    # Set AWS credentials in the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command for fetching user audit trail activity
    aws_command = [
        'aws', 'cloudtrail', 'lookup-events',
        '--region', config['region'],
        '--start-time', start_date.strftime("%Y-%m-%dT00:00:00Z"),
        '--end-time', current_date.strftime("%Y-%m-%dT23:59:59Z"),
        '--output', 'json'
    ]

    # Execute the AWS CLI command
    output = run_command(' '.join(aws_command))

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file)

print("Audit logs configuration evidence has been successfully created for all environments.")
