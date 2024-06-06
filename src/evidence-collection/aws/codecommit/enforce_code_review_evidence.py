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
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/"
    }
}

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.splitlines()

def main():
    for env_name, config in environments.items():
        # Set the AWS credentials for the environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']

        # Initialize an empty list to store JSON output
        output = []

        # Define the AWS CLI command
        aws_command = [
            'aws', 'codecommit', 'list-repositories',
            '--region', config['region'],
            '--output', 'json'
        ]

        # Run the command and capture the output
        try:
            command_output = run_command(aws_command)
            for line in command_output:
                output.append(json.loads(line))
        except Exception as e:
            print(f"Error running command for {env_name}: {e}")
            continue

        # Determine the output file path based on the environment
        if env_name == 'private-sector':
            output_file = config['private_sector_output_file']
        elif env_name == 'federal':
            output_file = config['federal_output_file']

        # Ensure the output directory exists
        os.makedirs(output_file, exist_ok=True)

        # Write the JSON output to the specified file path
        output_file_path = os.path.join(output_file, 'code_review_enforcement.json')
        with open(output_file_path, 'w') as f:
            json.dump(output, f, indent=4)

        print(f"Evidence for {env_name} environment saved to {output_file_path}")

if __name__ == "__main__":
    main()
