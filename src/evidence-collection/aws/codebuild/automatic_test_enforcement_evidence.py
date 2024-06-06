import os
import subprocess
from datetime import datetime
import json

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/private-sector/{current_date}.test-enforcement.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/federal/{current_date}.test-enforcement.json"
    }
}

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr}")
    return result.stdout.splitlines()

def main():
    for env_name, config in environments.items():
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']

        output = []

        # AWS CLI command to check for automatic test enforcement configuration
        aws_command = [
            'aws', 'codebuild', 'list-projects',  # Replace with actual command and subcommand
            '--output', 'json'
        ]

        try:
            command_output = run_command(aws_command)
            output.extend(command_output)
        except Exception as e:
            print(f"Error running command for {env_name} environment: {e}")
            continue

        output_dir = config['output_file']
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"{env_name}_automatic_test_enforcement.json")

        with open(output_file_path, 'w') as output_file:
            json.dump(output, output_file, indent=4)

        print(f"Evidence for {env_name} environment saved to {output_file_path}")

if __name__ == "__main__":
    main()
