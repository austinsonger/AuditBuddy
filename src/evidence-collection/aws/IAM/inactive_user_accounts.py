import os
import subprocess
import datetime
import json

current_year = datetime.datetime.now().year

environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/inactive_user_accounts.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/inactive_user_accounts.json"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def check_inactive_users(users, threshold_days=90):
    inactive_users = []
    current_time = datetime.datetime.now(datetime.timezone.utc)
    for user in users:
        if 'PasswordLastUsed' in user:
            last_used_time = datetime.datetime.fromisoformat(user['PasswordLastUsed'].replace('Z', '+00:00'))
            if (current_time - last_used_time).days > threshold_days:
                inactive_users.append(user)
        else:
            creation_time = datetime.datetime.fromisoformat(user['CreateDate'].replace('Z', '+00:00'))
            if (current_time - creation_time).days > threshold_days:
                inactive_users.append(user)
    return inactive_users

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

    inactive_users = check_inactive_users(users_output['Users'])
    output.extend(inactive_users)

    # Determine the output file based on environment
    if env_name == 'commercial':
        output_file = config['commercial_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
