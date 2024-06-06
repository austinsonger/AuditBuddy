import os
import subprocess
from datetime import datetime
import json

# Define the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Setup environments dictionary with AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/sensitive_data_network.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/sensitive_data_network.json"
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

    # Initialize an empty list to store JSON output
    output = []

    # AWS CLI command to list VPCs and their associated security and flow log settings
    vpc_command = [
        'aws', 'ec2', 'describe-vpcs',
        '--region', config['region'],
        '--output', 'json'
    ]
    security_group_command = [
        'aws', 'ec2', 'describe-security-groups',
        '--region', config['region'],
        '--output', 'json'
    ]
    flow_logs_command = [
        'aws', 'ec2', 'describe-flow-logs',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI commands
    vpc_info = run_command(vpc_command)
    security_group_info = run_command(security_group_command)
    flow_logs_info = run_command(flow_logs_command)

    # Append results to output list
    output.extend([
        {"VPC_Info": json.loads(vpc_info[0])},
        {"Security_Group_Info": json.loads(security_group_info[0])},
        {"Flow_Logs_Info": json.loads(flow_logs_info[0])}
    ])

    # Determine the output file based on environment
    output_file = config.get(f"{env_name}_output_file")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("Sensitive data network evidence files generated successfully.")
