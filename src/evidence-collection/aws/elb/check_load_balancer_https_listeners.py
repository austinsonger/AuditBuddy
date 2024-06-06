import os
import subprocess
from datetime import datetime
import json

# Define YEAR and DATE
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Define environments with AWS credentials and separate output files
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/aws/elb/{current_date}.load_balancers_https_listeners.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/aws/elb/{current_date}.load_balancers_https_listeners.json"
    }
}

# Function to run a command and capture output
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.split()

# Process each environment
for env_name, config in environments.items():
    print(f"Processing environment: {env_name}")
    print("-----------------------------------")

    # Set AWS credentials for the environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # Initialize an empty list for the JSON output
    output = []

    # Check Application Load Balancers (ALBs)
    print("Checking Application Load Balancers (ALBs)...")
    command = [
        'aws', 'elbv2', 'describe-load-balancers',
        '--query', 'LoadBalancers[*].LoadBalancerArn',
        '--output', 'text'
    ]
    alb_arns = run_command(command)
    for lb_arn in alb_arns:
        print(f"Checking ALB: {lb_arn}")
        command = [
            'aws', 'elbv2', 'describe-listeners',
            '--load-balancer-arn', lb_arn,
            '--query', 'Listeners[*].Protocol',
            '--output', 'text'
        ]
        listeners = run_command(command)
        https_status = "false" if any(protocol not in ['HTTPS', 'SSL'] for protocol in listeners) else "true"
        output.append({"load_balancer": lb_arn, "type": "ALB", "https_only": https_status})

    print("-----------------------------------")

    # Check Classic Load Balancers (CLBs)
    print("Checking Classic Load Balancers (CLBs)...")
    command = [
        'aws', 'elb', 'describe-load-balancers',
        '--query', 'LoadBalancerDescriptions[*].LoadBalancerName',
        '--output', 'text'
    ]
    clb_names = run_command(command)
    for lb_name in clb_names:
        print(f"Checking CLB: {lb_name}")
        command = [
            'aws', 'elb', 'describe-load-balancers',
            '--load-balancer-names', lb_name,
            '--query', 'LoadBalancerDescriptions[*].ListenerDescriptions[*].Listener.Protocol',
            '--output', 'text'
        ]
        listeners = run_command(command)
        https_status = "false" if any(protocol not in ['HTTPS', 'SSL'] for protocol in listeners) else "true"
        output.append({"load_balancer": lb_name, "type": "CLB", "https_only": https_status})

    # Determine the output file based on environment
    if env_name == 'commercial':
        output_file = config['commercial_output_file']
    elif env_name == 'federal':
        output_file = config['federal_output_file']

    # Write the output to a JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

    print(f"Output written to {output_file}")
    print("-----------------------------------")
    print()

print("All environment commands have been executed and outputs written to respective files.")
