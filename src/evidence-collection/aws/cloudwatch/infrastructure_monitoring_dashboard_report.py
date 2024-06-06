import os
import subprocess
import datetime
import json

# Current year for file path construction
current_year = datetime.datetime.now().year

# Environment settings for AWS credentials and output paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/monitoring_dashboard.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/monitoring_dashboard.json"
    }
}

def run_command(command):
    """ Run a shell command using subprocess and return the output as a list of strings. """
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip().split('\n')

# Main processing for each environment
for env_name, config in environments.items():
    # Set AWS environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to fetch dashboard names from CloudWatch
    aws_command = [
        'aws', 'cloudwatch', 'list-dashboards',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Execute command
    output = run_command(' '.join(aws_command))

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file)

