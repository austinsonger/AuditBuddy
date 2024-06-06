import os
import subprocess
from datetime import datetime
import json

# Define YEAR and DATE
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Set AWS credentials for the environment
os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
os.environ['AWS_DEFAULT_REGION'] = config['region']


# List all buckets
command = [
    'aws', 's3api', 'list-buckets',
    '--query', 'Buckets[*].Name',
    '--output', 'text'
]
buckets = subprocess.run(command, capture_output=True, text=True).stdout.split()

# Function to run a command and save output to a file
def save_to_file(command, output_file):
    result = subprocess.run(command, capture_output=True, text=True)
    with open(output_file, 'w') as file:
        file.write(result.stdout)

# Loop through each bucket and get its policy, encryption, versioning, and backup vaults
for bucket in buckets:
    print(f"Checking bucket: {bucket}")
    print("-----------------------------------")

    dir_path = f"/evidence-artifacts/{current_year}/private-sector/aws/S3/{bucket}"
    os.makedirs(dir_path, exist_ok=True)

    # Get bucket policy
    command = [
        'aws', 's3api', 'get-bucket-policy',
        '--bucket', bucket,
        '--query', 'Policy',
        '--output', 'json'
    ]
    output_file = f"/evidence-artifacts/{current_year}/private-sector/aws/S3/{bucket}/{current_date}.policy.json"
    save_to_file(command, output_file)

    # Get bucket encryption
    command = [
        'aws', 's3api', 'get-bucket-encryption',
        '--bucket', bucket,
        '--output', 'json'
    ]
    output_file = f"/evidence-artifacts/{current_year}/private-sector/aws/S3/{bucket}/{current_date}.encryption.json"
    save_to_file(command, output_file)

    # Get bucket versioning
    command = [
        'aws', 's3api', 'get-bucket-versioning',
        '--bucket', bucket,
        '--query', 'Status',
        '--output', 'text'
    ]
    versioning_status = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    versioning_status = "null" if versioning_status == "" else versioning_status
    with open(f"{dir_path}/{current_date}.versioning.json", 'w') as file:
        json.dump({"versioning": versioning_status}, file, indent=4)

    # Get backup vaults
    command = [
        'aws', 'backup', 'list-backup-vaults',
        '--query', 'BackupVaultList[*].BackupVaultName',
        '--output', 'json'
    ]
    output_file = f"/evidence-artifacts/{current_year}/private-sector/aws/S3/{bucket}/{current_date}.backup_vaults.json"
    save_to_file(command, output_file)

    print(f"Output written to {dir_path}")
    print("-----------------------------------")
    print()

print("All bucket information has been written to separate JSON files.")
