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
    This script collects information system monitoring logs for the following boundaries:
    - External boundary of the information system
    - Internal connections within the system

    It retrieves CloudFront access logs to monitor the external boundary and VPC Flow Logs to monitor internal connections. The logs are pulled from the past 365 days and saved as JSON files in the specified evidence artifacts directory.
    """
    command_runner = CommandRunner()
    start_time, end_time = get_time_range()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file paths
        external_boundary_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.external_boundary_logs.json"
        internal_connections_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.internal_connections_logs.json"

        # Define the AWS CLI commands with output file paths
        # Collect CloudFront logs for external boundary monitoring
        external_boundary_command = [
            'aws', 'logs', 'filter-log-events', '--log-group-name', 'CloudFront-Access-Logs',
            '--start-time', str(start_time), '--end-time', str(end_time),
            '--region', config.region, '--output', 'json'
        ]

        # Collect VPC Flow Logs for internal connections monitoring
        internal_connections_command = [
            'aws', 'logs', 'filter-log-events', '--log-group-name', 'VPC-Flow-Logs',
            '--start-time', str(start_time), '--end-time', str(end_time),
            '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, external_boundary_command, external_boundary_output_file)
        aws_handler.collect_evidence(command_runner, internal_connections_command, internal_connections_output_file)

if __name__ == "__main__":
    main()
