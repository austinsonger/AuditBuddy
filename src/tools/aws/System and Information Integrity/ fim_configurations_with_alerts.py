import sys
import os

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    """
    Evidence Description:
    This script collects evidence for file integrity monitoring (FIM) configurations, including notification settings and an example alert, by querying AWS Config and CloudWatch.

    Controls:
    - NIST 800-53 Requirement ID: SI-7 (Software, Firmware, and Information Integrity), CA-7 (Continuous Monitoring)
    - SOC 2 Control Number: CC7.2 (Change Detection), CC7.3 (Incident Management)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for AWS Config rules
        output_file_config_rules = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.fim_config_rules.json"

        # Define the AWS CLI command for describing AWS Config rules
        aws_command_config_rules = [
            'aws', 'configservice', 'describe-config-rules', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for AWS Config rules
        aws_handler.collect_evidence(command_runner, aws_command_config_rules, output_file_config_rules)

        # Generate the output file path for CloudWatch Alarms
        output_file_cw_alarms = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.fim_cloudwatch_alarms.json"

        # Define the AWS CLI command for describing CloudWatch alarms
        aws_command_cw_alarms = [
            'aws', 'cloudwatch', 'describe-alarms', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for CloudWatch alarms
        aws_handler.collect_evidence(command_runner, aws_command_cw_alarms, output_file_cw_alarms)

        # Generate the output file path for a sample CloudWatch alarm history
        output_file_cw_alarm_history = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.fim_cloudwatch_alarm_history.json"

        # Define the AWS CLI command for describing CloudWatch alarm history
        aws_command_cw_alarm_history = [
            'aws', 'cloudwatch', 'describe-alarm-history', '--region', config.region, '--output', 'json', '--max-records', '1'
        ]

        # Collect evidence for a sample CloudWatch alarm history
        aws_handler.collect_evidence(command_runner, aws_command_cw_alarm_history, output_file_cw_alarm_history)

if __name__ == "__main__":
    main()
