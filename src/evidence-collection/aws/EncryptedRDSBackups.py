import os
import subprocess
from datetime import datetime

# Get the current year and date
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Define the directories
private_sector_dir = f'/evidence-artifacts/private-sector/aws/lists/EncryptedRDSBackups/{current_year}/'
federal_dir = f'/evidence-artifacts/federal/aws/lists/EncryptedEBSVolumes/{current_year}/'

# Create directories if they do not exist
os.makedirs(private_sector_dir, exist_ok=True)
os.makedirs(federal_dir, exist_ok=True)

# Define the file paths
private_sector_snapshots_file = f'{private_sector_dir}{current_date}-db-snapshots.csv'
private_sector_instances_file = f'{private_sector_dir}{current_date}-db-instances.csv'
federal_snapshots_file = f'{federal_dir}{current_date}-db-snapshots.csv'
federal_instances_file = f'{federal_dir}{current_date}-db-instances.csv'

# Function to run AWS CLI command and save output to CSV
def run_aws_command(command, output_file):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        with open(output_file, 'w') as file:
            file.write(result.stdout)
    else:
        print(f"Error running command: {' '.join(command)}")
        print(result.stderr)

# AWS CLI commands
commands = [
    (
        ['aws', 'rds', 'describe-db-snapshots', '--output', 'json', '--query',
         'DBSnapshots[*].[DBSnapshotIdentifier,DBInstanceIdentifier,Encrypted,SnapshotCreateTime,KmsKeyId]'],
        private_sector_snapshots_file
    ),
    (
        ['aws', 'rds', 'describe-db-instances', '--output', 'json', '--query',
         'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,StorageEncrypted,KmsKeyId]'],
        private_sector_instances_file
    ),
    (
        ['aws', 'rds', 'describe-db-snapshots', '--output', 'json', '--query',
         'DBSnapshots[*].[DBSnapshotIdentifier,DBInstanceIdentifier,Encrypted,SnapshotCreateTime,KmsKeyId]'],
        federal_snapshots_file
    ),
    (
        ['aws', 'rds', 'describe-db-instances', '--output', 'json', '--query',
         'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,StorageEncrypted,KmsKeyId]'],
        federal_instances_file
    )
]

# Run the commands and save the output
for command, output_file in commands:
    run_aws_command(command, output_file)

print(f"Completed. Files saved to {private_sector_dir} and {federal_dir}.")
