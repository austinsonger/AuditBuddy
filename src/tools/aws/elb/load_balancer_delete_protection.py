import os
import subprocess
from datetime import datetime
import json

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

for env_name, config in environments.items():
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    output = []

    # AWS CLI command to describe load balancers and check for delete protection
    aws_command = [
        'aws', 'elbv2', 'describe-load-balancer-attributes',
        '--region', config['region'],
        '--query', 'LoadBalancers[*].{LoadBalancerArn:LoadBalancerArn,DeletionProtectionEnabled:Attributes[?Key==`deletion_protection.enabled`].Value | [0]}',
        '--output', 'json'
    ]

    command_output = run_command(aws_command)
    output.extend(command_output)

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file'] + "load_balancer_delete_protection.json"
    elif env_name == 'federal':
        output_file = config['federal_output_file'] + "load_balancer_delete_protection.json"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
