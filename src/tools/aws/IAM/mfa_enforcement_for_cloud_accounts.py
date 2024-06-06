import os
import subprocess
import datetime
import json

current_year = datetime.datetime.now().year

environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/mfa_enforcement_for_cloud_accounts.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/mfa_enforcement_for_cloud_accounts.json"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def check_mfa_enforcement(users):
    mfa_enabled_users = []
    for user in users:
        list_mfa_devices_command = [
            'aws', 'iam', 'list-mfa-devices',
            '--user-name', user['UserName'],
            '--region', user['Arn'].split(':')[3],
            '--output', 'json'
        ]
        mfa_devices_output = json.loads("\n".join(run_command(list_mfa_devices_command)))
        if mfa_devices_output['MFADevices']:
            mfa_enabled_users.append(user)
    return mfa_enabled_users

for env_name, config in environments.items():
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    output = []

    # AWS CLI command to list IAM users
    list_users_command = [
        'aws', 'iam', 'list-users',
        '--region', config['region'],
        '--output', 'json'
    ]
    users_output = json.loads("\n".join(run_command(list_users_command)))

    mfa_enabled_users = check_mfa_enforcement(users_output['Users'])
    output.extend(mfa_enabled_users)

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
