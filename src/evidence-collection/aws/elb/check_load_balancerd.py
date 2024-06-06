import os
import subprocess
from datetime import datetime
import json

# Define YEAR and DATE
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')
dir_path = f"evidence-artifacts/{current_year}/commercial/aws/elb/"

# Ensure the directory exists
os.makedirs(dir_path, exist_ok=True)

# Initialize an empty list for the JSON output
output = []

# Check Application Load Balancers (ALBs)
print("Checking Application Load Balancers (ALBs)...")
command = [
    'aws', 'elbv2', 'describe-load-balancers',
    '--query', 'LoadBalancers[*].LoadBalancerArn',
    '--output', 'text'
]
alb_arns = subprocess.run(command, capture_output=True, text=True).stdout.split()
for lb_arn in alb_arns:
    print(f"Checking ALB: {lb_arn}")
    command = [
        'aws', 'elbv2', 'describe-load-balancer-attributes',
        '--load-balancer-arn', lb_arn,
        '--query', 'Attributes[?Key==`access_logs.s3.enabled`].Value',
        '--output', 'text'
    ]
    access_logs_enabled = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    access_logs_status = "enabled" if access_logs_enabled == "true" else "not enabled"
    output.append({"load_balancer": lb_arn, "type": "ALB", "access_logs": access_logs_status})

print("-----------------------------------")

# Check Classic Load Balancers (CLBs)
print("Checking Classic Load Balancers (CLBs)...")
command = [
    'aws', 'elb', 'describe-load-balancers',
    '--query', 'LoadBalancerDescriptions[*].LoadBalancerName',
    '--output', 'text'
]
clb_names = subprocess.run(command, capture_output=True, text=True).stdout.split()
for lb_name in clb_names:
    print(f"Checking CLB: {lb_name}")
    command = [
        'aws', 'elb', 'describe-load-balancer-attributes',
        '--load-balancer-name', lb_name,
        '--query', 'LoadBalancerAttributes.AccessLog.Enabled',
        '--output', 'text'
    ]
    access_logs_enabled = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    access_logs_status = "enabled" if access_logs_enabled == "true" else "not enabled"
    output.append({"load_balancer": lb_name, "type": "CLB", "access_logs": access_logs_status})

# Write the output to a JSON file
output_file = f"{dir_path}/{current_date}.load_balancers.json"
with open(output_file, 'w') as file:
    json.dump(output, file, indent=4)

print(f"Output written to {output_file}")
