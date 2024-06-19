# File: main.py

import sys
import os

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Define the AWS CLI commands and output file paths
        commands = [
            {
                "description": "Describe CloudTrail trails",
                "aws_command": ['aws', 'cloudtrail', 'describe-trails', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-trails.json"
            },
            {
                "description": "Get CloudTrail trail status",
                "aws_command": ['aws', 'cloudtrail', 'get-trail-status', '--name', '<trail-name>', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.trail-status-<trail-name>.json"
            },
            {
                "description": "Describe CloudWatch log groups",
                "aws_command": ['aws', 'logs', 'describe-log-groups', '--region', config.region, '--output', 'json'],
                "output_file": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe-log-groups.json"
            },
            {
                "description": "Get CloudWatch log group retention policy",
                "aws_command": ['aws', 'logs', 'describe-log-groups', '--region', config.region, '--output', 'json'],
                "output_file_template": f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.log-group-retention-<log-group-name>.json"
            }
        ]

        for command in commands:
            if '<trail-name>' in command["aws_command"]:
                trails = aws_handler.get_cloudtrail_trails(command_runner)
                for trail in trails:
                    trail_command = command["aws_command"].copy()
                    trail_command[4] = trail  # Replace <trail-name> with actual trail name
                    output_file = command["output_file_template"].replace('<trail-name>', trail)
                    aws_handler.collect_evidence(command_runner, trail_command, output_file)
            elif '<log-group-name>' in command["aws_command"]:
                log_groups = aws_handler.get_cloudwatch_log_groups(command_runner)
                for log_group in log_groups:
                    log_group_command = command["aws_command"].copy()
                    log_group_command[4] = log_group  # Replace <log-group-name> with actual log group name
                    output_file = command["output_file_template"].replace('<log-group-name>', log_group)
                    aws_handler.collect_evidence(command_runner, log_group_command, output_file)
            else:
                aws_handler.collect_evidence(command_runner, command["aws_command"], command["output_file"])

if __name__ == "__main__":
    main()

"""
NIST 800-53 Requirement ID:
- AU-4: Audit Storage Capacity
- AU-11: Audit Record Retention

SOC 2 Control Number:
- CC7.3: System Monitoring
- CC7.4: Incident Management
"""
