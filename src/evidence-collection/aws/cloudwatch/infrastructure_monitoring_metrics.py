import os
import subprocess
from datetime import datetime
import json

# Define the current year
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set up environment dictionary with AWS credentials and output file paths
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'private_sector_output_file': f"/evidence-artifacts/{current_year}/private-sector/{current_date}.monitoring-metrics.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/{current_date}.monitoring-metrics.json"
    }
}

def run_command(command):
    """ Run a shell command and return the output as a list of strings. """
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.splitlines()

def main():
    for env_name, config in environments.items():
        # Set AWS credentials for the environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']

        # Define the AWS CLI command for fetching CloudWatch metrics
        aws_command = [
            'aws', 'cloudwatch', 'list-metrics',
            '--namespace', 'AWS/EC2',
            '--metric-name', 'CPUUtilization',
            '--region', config['region'],
            '--output', 'json'
        ]

        # Run the command and store the output
        output = run_command(aws_command)

        # Determine the output file based on environment
        if env_name == 'private-sector':
            output_file = config['private_sector_output_file']
        elif env_name == 'federal':
            output_file = config['federal_output_file']

        # Ensure the directory exists
        os.makedirs(output_file, exist_ok=True)

        # Write the output to the file
        with open(f"{output_file}metrics_output.json", "w") as file:
            json.dump(output, file, indent=4)

if __name__ == "__main__":
    main()
