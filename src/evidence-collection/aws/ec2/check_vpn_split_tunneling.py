import os
import subprocess
import datetime
import json

# Current year
current_year = datetime.datetime.now().year

# Environment setup
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/vpn_config.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/vpn_config.json"
    }
}

def run_command(command):
    """Execute a shell command and return the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()

# Iterate over each environment
for env_name, config in environments.items():
    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to check VPN configuration
    aws_command = [
        'aws', 'ec2', 'describe-vpn-connections',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Initialize an empty list to store JSON output
    output = []

    # Execute AWS CLI command
    output = run_command(aws_command)

    # Determine the output file based on environment
    output_file = config[env_name + '_output_file'] if (env_name + '_output_file') in config else None

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as f:
        json.dump(output, f)

print("Script execution completed. VPN configurations checked and results saved.")
