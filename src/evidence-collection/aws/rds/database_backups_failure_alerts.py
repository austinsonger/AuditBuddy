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
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/database_backups_failure_alerts.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/database_backups_failure_alerts.json"
    }
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def get_backup_failure_alerts():
    describe_events_command = [
        'aws', 'rds', 'describe-events',
        '--source-type', 'db-instance',
        '--event-categories', 'backup',
        '--duration', '360',
        '--output', 'json'
    ]
    events_output = json.loads("\n".join(run_command(describe_events_command)))
    return events_output

for env_name, config in environments.items():
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    output = []

    backup_failure_alerts = get_backup_failure_alerts()
    output.append(backup_failure_alerts)

    # Determine the output file based on environment
    if env_name == 'commercial':
        output_file = config['commercial_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)

print("Evidence collection completed.")
