import os
import subprocess
import datetime
import json

current_year = datetime.datetime.now().year

environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/bastion_host_configuration.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/bastion_host_configuration.json"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def get_bastion_host_configuration():
    describe_instances_command = [
        'aws', 'ec2', 'describe-instances',
        '--filters', 'Name=tag:Name,Values=bastion-host',
        '--region', 'us-east-1',
        '--output', 'json'
    ]
    instances_output = json.loads("\n".join(run_command(describe_instances_command)))
    return instances_output

for env_name, config in environments.items():
    access_key = config['access_key']
    secret_key = config['secret_key']

    if access_key is None or secret_key is None:
        print(f"Missing credentials for {env_name}, skipping...")
        continue

    os.environ['AWS_ACCESS_KEY_ID'] = access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    output = []

    bastion_host_configuration = get_bastion_host_configuration()
    output.append(bastion_host_configuration)

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
