import os
import subprocess
import datetime
import json

# Define the current year and date
current_year = datetime.datetime.now().year
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Define environments dictionary
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/aws/rds/{current_date}_encrypted_backup_evidence.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/aws/rds/{current_date}_encrypted_backup_evidence.json"
    }
}

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

for env_name, config in environments.items():
    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Initialize an empty list to store JSON output
    output = []

    # Run AWS CLI command to list RDS snapshots and their encryption status
    command = "aws rds describe-db-snapshots --query 'DBSnapshots[*].{SnapshotIdentifier:DBSnapshotIdentifier,Encrypted:Encrypted}'"
    command_output = run_command(command)
    
    for line in command_output:
        try:
            snapshot_info = json.loads(line)
            output.append(snapshot_info)
        except json.JSONDecodeError:
            continue
    
    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file_path, 'w') as f:
        json.dump(output, f, indent=4)

    print(f"Evidence file created for {env_name} environment at {output_file_path}")
