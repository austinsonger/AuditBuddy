import os
import subprocess
import datetime
import json

# Current year calculation
current_year = datetime.datetime.now().year

# Environment configuration dictionary
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.splitlines()

# Iterate over environments to configure AWS CLI and save output
for env_name, config in environments.items():
    # Set AWS environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to get information about patch management configuration
    aws_command = [
        'aws', 'ssm', 'describe-patch-baselines',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run AWS CLI command
    output = run_command(' '.join(aws_command))

    # Determine the output file path based on the environment
    if env_name == 'commercial':
        output_file = config['commercial_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Ensure the output directory exists
    os.makedirs(output_file, exist_ok=True)

    # Write the JSON output to the specified file path
    with open(f"{output_file}patch_management_config.json", 'w') as file:
        json.dump(output, file)

print("Evidence generated for patch management tool configuration.")
