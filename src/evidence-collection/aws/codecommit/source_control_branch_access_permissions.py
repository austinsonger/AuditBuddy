import os
import subprocess
import datetime
import json

# Current year
current_year = datetime.datetime.now().year

# Environments dictionary
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/private-sector/access_permissions.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/federal/access_permissions.json"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

# Iterate over each environment
for env_name, config in environments.items():
    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']
    
    # AWS CLI command to list branch access permissions (modify as necessary)
    aws_command = [
        'aws', 'codecommit', 'get-branch',
        '--repository-name', 'YourRepositoryName',
        '--branch-name', 'main',
        '--output', 'json'
    ]
    
    # Run the AWS CLI command
    output = run_command(aws_command)
    
    # Parse the JSON output
    json_output = [json.loads(line) for line in output]
    
    # Determine the output file path
    output_file_path = config['output_file']
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # Write the JSON output to the specified file
    with open(output_file_path, 'w') as f:
        json.dump(json_output, f, indent=4)

print("Evidence collection complete.")
