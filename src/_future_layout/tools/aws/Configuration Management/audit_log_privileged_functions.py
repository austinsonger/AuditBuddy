# [main.py]
import sys
import os
from datetime import datetime, timedelta

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler


def get_time_range():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=365)
    return int(start_time.timestamp() * 1000), int(end_time.timestamp() * 1000)

def main():
    """
    This script collects audit logs showing the monitoring of privileged functions as they are executed.

    It retrieves CloudTrail logs to monitor the execution of privileged functions. The logs are pulled
    from the past 365 days and saved as JSON files in the specified evidence artifacts directory.
    """
    command_runner = CommandRunner()
    start_time, end_time = get_time_range()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        privileged_functions_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.privileged_functions_logs.json"

        # Define the AWS CLI command with output file path
        # Collect CloudTrail logs for privileged function monitoring
        privileged_functions_command = [
            'aws', 'logs', 'filter-log-events', '--log-group-name', 'CloudTrail-Logs',
            '--start-time', str(start_time), '--end-time', str(end_time),
            '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, privileged_functions_command, privileged_functions_output_file)

if __name__ == "__main__":
    main()
