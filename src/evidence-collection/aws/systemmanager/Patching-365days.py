import subprocess
import json
from datetime import datetime, timedelta
import re
import os

# Define the date format
current_date_str = datetime.utcnow().strftime('%Y-%b-%d')

# Define the output file paths with the current date
all_patches_file = f'lists/{current_date_str}.ssm-patch-manager_all-patches.json'
filtered_patches_file = f'lists/{current_date_str}.ssm-patch-manager_available-patches.json'

# Create directories if they do not exist
os.makedirs(os.path.dirname(all_patches_file), exist_ok=True)
os.makedirs(os.path.dirname(filtered_patches_file), exist_ok=True)

# Run the AWS CLI command to get all patches
command = [
    'aws', 'ssm', 'describe-available-patches',
    '--region', 'us-east-1',
    '--filters', 'Key=PRODUCT,Values=AmazonLinux2',
    '--output', 'json'
]

with open(all_patches_file, 'w') as file:
    subprocess.run(command, stdout=file)

# Load the data from the output file
with open(all_patches_file, 'r') as file:
    data = json.load(file)

# Define the date range for the last 365 days
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=365)

# Function to parse date strings with time zone info
def parse_date(date_str):
    # Match the date part and ignore the timezone offset
    match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', date_str)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S')
    else:
        return None

# Filter patches by date range
filtered_patches = [
    patch for patch in data['Patches']
    if start_date <= parse_date(patch['ReleaseDate']) <= end_date
]

# Save the filtered patches to a new file
with open(filtered_patches_file, 'w') as file:
    json.dump({'Patches': filtered_patches}, file, indent=4)

print(f"Filtered {len(filtered_patches)} patches within the date range.")
