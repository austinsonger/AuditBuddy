import os
import subprocess
import datetime
import json

# Define the current year
current_year = datetime.datetime.now().year

# Setup environments dictionary with AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/replay_resistant_auth.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/replay_resistant_auth.json"
    }
}

# Function to run shell commands and capture the output
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    if result.returncode == 0:
        return result.stdout.strip().split('\n')
    else:
        raise Exception(f"Command failed: {result.stderr}")

# Iterate over each environment to set credentials and generate output
for env_name, config in environments.items():
    # Set the AWS credentials for the current environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to list all IAM users and their MFA devices
    aws_command = [
        'aws', 'iam', 'list-mfa-devices',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command to gather MFA device information for IAM users
    mfa_info = run_command(aws_command)
    mfa_data = json.loads(mfa_info[0])

    # Initialize an empty list to store MFA details
    output = []

    # Extract and add MFA details to the output list
    for mfa_detail in mfa_data['MFADevices']:
        output.append({
            'UserName': mfa_detail['UserName'],
            'SerialNumber': mfa_detail['SerialNumber'],
            'EnableDate': mfa_detail['EnableDate']
        })

    # Determine the output file based on environment
    output_file = config.get(f"{env_name}_output_file")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("Replay-resistant authentication evidence files generated successfully.")
