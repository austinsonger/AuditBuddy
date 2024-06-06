import os
import subprocess
import datetime
import json

# Set current year
current_year = datetime.datetime.now().year

# Environments dictionary
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/commercial/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/federal/"
    }
}

def run_command(command):
    """Runs a given shell command and returns the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.splitlines()

# Iterate over each environment
for env_name, config in environments.items():
    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']
    
    # Initialize an empty list to store JSON output
    output = []

    # AWS CLI command (replace placeholders with actual values)
    aws_command = [
        'aws', 'codepipeline', 'get-pipeline-state',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command
    command_output = run_command(aws_command)

    # Add command output to the list
    output.extend(command_output)
    
    # Determine the output file based on environment
    output_file = config['output_file'] + 'cicd_tool_configuration.json'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("CI/CD tool configuration evidence generated successfully.")
