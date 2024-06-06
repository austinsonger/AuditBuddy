import os
import subprocess
import datetime
import json

# Set the current year
current_year = datetime.datetime.now().year

# Environments setup
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/session_policies.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/session_policies.json"
    }
}

def run_command(command):
    """Run a shell command using subprocess and return the output as a list of strings."""
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()

def main():
    for env_name, config in environments.items():
        # Set AWS credentials for the current environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']

        # AWS CLI command to get session policies (for example purposes)
        aws_command = [
            'aws', 'iam', 'list-policies',
            '--scope', 'Local',
            '--output', 'json'
        ]

        # Initialize output list and execute command
        output = run_command(aws_command)

        # Parse JSON and filter for session policies requiring re-authentication (dummy filter)
        session_policies = [policy for policy in json.loads(''.join(output)) if 'idle_timeout' in policy]

        # Determine the output file based on environment
        output_file = config[f"{env_name}_output_file"]
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the JSON output to the specified file path
        with open(output_file, 'w') as file:
            json.dump(session_policies, file, indent=4)

if __name__ == '__main__':
    main()
