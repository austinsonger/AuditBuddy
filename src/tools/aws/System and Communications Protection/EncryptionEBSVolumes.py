import os
import subprocess
from datetime import datetime

# Get the current year and date
current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Define the directories
private_sector_dir = f'/evidence-artifacts/private-sector/aws/lists/EncryptedEBSVolumes/{current_year}/'
federal_dir = f'/evidence-artifacts/federal/aws/lists/EncryptedEBSVolumes/{current_year}/'

# Create directories if they do not exist
os.makedirs(private_sector_dir, exist_ok=True)
os.makedirs(federal_dir, exist_ok=True)

# Define the file paths
private_sector_volumes_file = f'{private_sector_dir}{current_date}-encrypted_volumes.csv'
federal_volumes_file = f'{federal_dir}{current_date}-encrypted_volumes.csv'

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
        ['aws', 'ec2', 'describe-volumes', '--query', 'Volumes[?Encrypted==`true`]', '--output', 'json'],
        private_sector_volumes_file
    ),
    (
        ['aws', 'ec2', 'describe-volumes', '--query', 'Volumes[?Encrypted==`true`]', '--output', 'json'],
        federal_volumes_file
    )
]

# Run the commands and save the output
for command, output_file in commands:
    run_aws_command(command, output_file)

print(f"Completed. Files saved to {private_sector_dir} and {federal_dir}.")
