# main.py
import sys
import os
from datetime import datetime, timedelta

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    """
    Main function to collect a list of all installed patches applied to information systems in the past 12 months.
    The evidence is gathered from AWS Systems Manager (SSM) and saved to JSON files.
    """
    command_runner = CommandRunner()

    # Calculate the date 12 months ago
    start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.installed_patches.json"

        # Define the AWS CLI command to list all managed instances
        list_instances_command = [
            'aws', 'ssm', 'describe-instance-information', '--region', config.region, '--output', 'json'
        ]

        # Collect instance information
        instance_info = command_runner.run(list_instances_command)
        instances = json.loads(instance_info).get('InstanceInformationList', [])

        # Initialize a list to store all patch data
        all_patch_data = []

        # Iterate over each instance to collect patch information
        for instance in instances:
            instance_id = instance['InstanceId']

            # Define the AWS CLI command for patch compliance information with date filtering
            patch_compliance_command = [
                'aws', 'ssm', 'list-compliance-items', '--resource-id', instance_id, '--resource-type', 'ManagedInstance',
                '--filters', f"Key=ComplianceType,Values=Patch", f"Key=ExecutionStartTime,Values={start_date}", '--region', config.region, '--output', 'json'
            ]

            # Collect patch compliance data for the instance
            patch_data = command_runner.run(patch_compliance_command)
            patch_compliance = json.loads(patch_data).get('ComplianceItems', [])

            # Add patch compliance data to the list
            all_patch_data.extend(patch_compliance)

        # Write all collected patch data to the output file
        with open(output_file, 'w') as f:
            json.dump(all_patch_data, f, indent=4)

if __name__ == "__main__":
    main()
