import os
import subprocess
import datetime
import json

# Get the current year
current_year = datetime.datetime.now().year

# Define the environments dictionary
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/commercial/databases_public_access.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/federal/databases_public_access.json"
    }
}

def run_command(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr}")
    return result.stdout.splitlines()

# Iterate over each environment
for env_name, config in environments.items():
    # Set the AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']
    
    # Initialize an empty list to store JSON output
    output = []
    
    # Define the AWS CLI command
    aws_command = [
        'aws', 'rds', 'describe-db-instances',
        '--filters', 'Name=db-instance-publicly-accessible,Values=false',
        '--output', 'json'
    ]
    
    # Run the command and capture the output
    command_output = run_command(aws_command)
    for line in command_output:
        output.append(json.loads(line))
    
    # Determine the output file path based on the environment
    output_file = config['output_file']
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the JSON output to the specified file path
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence generated successfully.")
