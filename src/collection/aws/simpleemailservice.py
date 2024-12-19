import os
import subprocess
import datetime
import json

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.utcnow().isoformat()
# Replace with actual configuration set name and resource ARN
config_set_name = 'YOUR_CONFIG_SET_NAME'
resource_arn = 'YOUR_RESOURCE_ARN'


# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            'identities': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-sesv2_email_identities.json",
            'configuration_sets': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-sesv2_configuration_sets.json",
            'dedicated_ips': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-sesv2_dedicated_ips.json",
            'event_destinations': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-sesv2_event_destinations.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-sesv2_tags.json"
        }
    },
    'federal': {
        'access_key': os.getenv('DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-west-2',
        'output_files': {
            'identities': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-sesv2_email_identities.json",
            'configuration_sets': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-sesv2_configuration_sets.json",
            'dedicated_ips': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-sesv2_dedicated_ips.json",
            'event_destinations': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-sesv2_event_destinations.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-sesv2_tags.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Fetch all SES email identities
def fetch_email_identities(config, output_file):
    identities_data = run_command(['aws', 'sesv2', 'list-email-identities', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(identities_data, f, indent=4)

# Fetch configuration sets
def fetch_configuration_sets(config, output_file):
    config_sets_data = run_command(['aws', 'sesv2', 'list-configuration-sets', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(config_sets_data, f, indent=4)

# Fetch dedicated IPs
def fetch_dedicated_ips(config, output_file):
    dedicated_ips_data = run_command(['aws', 'sesv2', 'list-dedicated-ips', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(dedicated_ips_data, f, indent=4)

# Fetch event destinations for a configuration set
def fetch_event_destinations(config, output_file, config_set_name):
    event_destinations_data = run_command([
        'aws', 'sesv2', 'list-event-destinations',
        '--configuration-set-name', config_set_name,
        '--region', config['region'],
        '--output', 'json'
    ])
    with open(output_file, 'w') as f:
        json.dump(event_destinations_data, f, indent=4)

# Fetch tags for a specific SES resource
def fetch_sesv2_tags(config, output_file, resource_arn):
    tags_data = run_command(['aws', 'sesv2', 'list-tags-for-resource', '--resource-arn', resource_arn, '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# Main function to execute each evidence collection task
def main():
    for env_name, config in environments.items():
        # Set AWS environment variables for each environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']
        
        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Collect evidence for AWS SES v2 configurations
        fetch_email_identities(config, config['output_files']['identities'])
        fetch_configuration_sets(config, config['output_files']['configuration_sets'])
        fetch_dedicated_ips(config, config['output_files']['dedicated_ips'])
        fetch_event_destinations(config, config['output_files']['event_destinations'], config_set_name)
        fetch_sesv2_tags(config, config['output_files']['tags'], resource_arn)

    print("AWS SES v2 configuration evidence collection completed.")

# Execute main function
if __name__ == "__main__":
    main()
