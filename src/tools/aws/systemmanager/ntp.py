import os
import subprocess
from datetime import datetime

# Define YEAR and DATE variables
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Define the environments and their respective AWS credentials
environments = {
    'private-sector': {
        'access_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_PRIVSEC_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/private-sector/aws/systemmanager/{current_date}.current-time.txt",
        'command': [
            'aws', 'ssm', 'send-command',
            '--document-name', 'AWS-RunShellScript',
            '--targets', 'Key=tag:Name,Values=cmd-prod1-east1-eks1-generic',
            '--parameters', 'commands=["cat /etc/ntp.conf"]',
            '--output', 'text'
        ]
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_file': f"/evidence-artifacts/{current_year}/federal/aws/systemmanager/{current_date}.current-time.txt",
        'command': [
            'aws', 'ssm', 'send-command',
            '--document-name', 'AWS-RunShellScript',
            '--targets', 'Key=tag:Name,Values=cmd-prod1-east1-eks1-generic',
            '--parameters', 'commands=["cat /etc/ntp.conf"]',
            '--output', 'text'
        ]
    }
}

# Log file paths
logfile = "evidence.log"
error_logfile = "errors.log"

# Function to log messages
def log_message(message):
    with open(logfile, 'a') as log:
        log.write(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# Function to log error messages
def error_log_message(message):
    with open(error_logfile, 'a') as log:
        log.write(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] Error: {message}\n")

# Function to log current system time using AWS CLI for a given environment
def log_current_time(environment, config):
    output_file = config['output_file']
    
    # Create directories if they do not exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']
    
    # Print the command being executed for clarity
    print(f"Running command for {environment} environment: {' '.join(config['command'])}")
    
    # Run the command and capture output
    result = subprocess.run(config['command'], capture_output=True, text=True)
    
    # Save output to file and handle logging
    with open(output_file, 'w') as file:
        file.write(result.stdout)
    
    if result.returncode != 0:
        error_log_message(f"Failed to log current system time via AWS CLI for {environment} environment.")
    else:
        log_message(f"Current system time logged successfully via AWS CLI for {environment} environment.")
    
    # Check if the file was created successfully
    if os.path.isfile(output_file):
        log_message(f"File created successfully: {output_file}")
    else:
        error_log_message(f"Failed to create file: {output_file}")

# Log current system time for both private-sector and federal environments
for env, config in environments.items():
    if not config['access_key'] or not config['secret_key']:
        error_log_message(f"Missing AWS credentials for {env} environment.")
        continue
    log_current_time(env, config)

print("Completed. Output saved to respective directories.")
