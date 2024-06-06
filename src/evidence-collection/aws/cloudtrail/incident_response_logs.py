import os
import subprocess
from datetime import datetime
import json

# Current year for file path construction
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Environment settings for AWS credentials and output paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/{current_date}.incident_response_logs.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/{current_date}.incident_response_logs.json"
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

    # AWS CLI command to fetch incident response logs
    aws_command = [
        'aws', 'cloudtrail', 'lookup-events',
        '--region', config['region'],
        '--lookup-attributes', 'AttributeKey=EventName,AttributeValue=StopLogging',
        '--output', 'json'
    ]

    # Execute command
    output = run_command(' '.join(aws_command))

    # Determine the output file based on environment
    output_file = config.get(f"{env_name}_output_file")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file)
