import os
import subprocess
from datetime import datetime
import json

# Current year for file paths
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Environment setup for AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/tif_evidence.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/tif_evidence.json"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, text=True, capture_output=True, shell=True)
    return result.stdout.strip().split('\n')

# Processing each environment
for env_name, config in environments.items():
    # Set the AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to get threat intelligence feeds
    aws_command = [
        'aws', 'guardduty', 'list-threat-intel-sets',
        '--detector-id', '<detector-id>',  # Replace '<detector-id>' with the actual detector ID
        '--region', config['region'],
        '--output', 'json'
    ]

    # Running the command and collecting output
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
