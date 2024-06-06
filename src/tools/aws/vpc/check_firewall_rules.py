import os
import subprocess
from datetime import datetime

# Define YEAR and DATE
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')
dir_path = f"lists/{current_year}/firewall_rules"

# Ensure the directory exists
os.makedirs(dir_path, exist_ok=True)

# Function to run a command and save output to a file
def save_to_file(command, output_file):
    result = subprocess.run(command, capture_output=True, text=True)
    with open(output_file, 'w') as file:
        file.write(result.stdout)

# Check Security Groups
print("Checking Security Groups...")
command = ['aws', 'ec2', 'describe-security-groups', '--query', 'SecurityGroups[*].GroupId', '--output', 'text']
security_groups = subprocess.run(command, capture_output=True, text=True).stdout.split()
for sg_id in security_groups:
    print(f"Describing Security Group: {sg_id}")
    command = ['aws', 'ec2', 'describe-security-groups', '--group-ids', sg_id, '--output', 'json']
    output_file = f"{dir_path}/{current_date}.security_group_{sg_id}.json"
    save_to_file(command, output_file)

# Check Network ACLs
print("Checking Network ACLs...")
command = ['aws', 'ec2', 'describe-network-acls', '--query', 'NetworkAcls[*].NetworkAclId', '--output', 'text']
network_acls = subprocess.run(command, capture_output=True, text=True).stdout.split()
for nacl_id in network_acls:
    print(f"Describing Network ACL: {nacl_id}")
    command = ['aws', 'ec2', 'describe-network-acls', '--network-acl-ids', nacl_id, '--output', 'json']
    output_file = f"{dir_path}/{current_date}.network_acl_{nacl_id}.json"
    save_to_file(command, output_file)

# Check AWS WAF Web ACLs
print("Checking AWS WAF Web ACLs...")
command = ['aws', 'wafv2', 'list-web-acls', '--scope', 'REGIONAL', '--query', 'WebACLs[*].Id', '--output', 'text']
web_acls = subprocess.run(command, capture_output=True, text=True).stdout.split()
for web_acl_id in web_acls:
    print(f"Describing Web ACL: {web_acl_id}")
    command = ['aws', 'wafv2', 'get-web-acl', '--scope', 'REGIONAL', '--id', web_acl_id, '--output', 'json']
    output_file = f"{dir_path}/{current_date}.web_acl_{web_acl_id}.json"
    save_to_file(command, output_file)

print(f"Firewall rules configuration has been written to JSON files in {dir_path}.")
