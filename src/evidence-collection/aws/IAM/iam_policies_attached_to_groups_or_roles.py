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
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/iam_policies_attached_to_groups_or_roles.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/iam_policies_attached_to_groups_or_roles.json"
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

    # AWS CLI command to list users
    list_users_command = [
        'aws', 'iam', 'list-users',
        '--region', config['region'],
        '--output', 'json'
    ]
    users_output = json.loads("\n".join(run_command(list_users_command)))

    for user in users_output['Users']:
        user_name = user['UserName']
        list_attached_policies_command = [
            'aws', 'iam', 'list-attached-user-policies',
            '--user-name', user_name,
            '--region', config['region'],
            '--output', 'json'
        ]
        attached_policies_output = json.loads("\n".join(run_command(list_attached_policies_command)))
        
        if attached_policies_output['AttachedPolicies']:
            output.append({
                'UserName': user_name,
                'AttachedPolicies': attached_policies_output['AttachedPolicies']
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
