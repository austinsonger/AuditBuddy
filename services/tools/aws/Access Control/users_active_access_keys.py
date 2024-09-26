import os
import subprocess
import datetime
import json

current_year = datetime.datetime.now().year

environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/users_active_access_keys.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/users_active_access_keys.json"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def check_active_keys(user_keys):
    active_keys = [key for key in user_keys if key['Status'] == 'Active']
    return len(active_keys) > 1

for env_name, config in environments.items():
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    output = []

    # AWS CLI command to list users
    list_users_command = [
        'aws', 'iam', 'list-users',
        '--region', config['region'],
        '--output', 'json'
    ]
    users_output = json.loads("\n".join(run_command(list_users_command)))

    for user in users_output['Users']:
        user_name = user['UserName']
        list_access_keys_command = [
            'aws', 'iam', 'list-access-keys',
            '--user-name', user_name,
            '--region', config['region'],
            '--output', 'json'
        ]
        access_keys_output = json.loads("\n".join(run_command(list_access_keys_command)))
        
        if check_active_keys(access_keys_output['AccessKeyMetadata']):
            output.append({
                'UserName': user_name,
                'ActiveAccessKeys': access_keys_output['AccessKeyMetadata']
            })

    # Determine the output file based on environment
    if env_name == 'private-sector':
        output_file = config['private_sector_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
