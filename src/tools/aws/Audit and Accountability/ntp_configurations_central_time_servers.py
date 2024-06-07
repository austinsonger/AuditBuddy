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
    This script collects evidence of NTP (Network Time Protocol) configurations from central time servers by querying various AWS services.

    Controls:
    - NIST 800-53 Requirement ID: AU-8 (Time Stamps), SC-45 (System Time Synchronization)
    - SOC 2 Control Number: CC5.3 (System Operations)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for EC2 instances NTP configuration
        output_file_ntp_config = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.ntp_configurations.json"

        # Define the AWS CLI command for describing EC2 instances
        aws_command_ec2_instances = [
            'aws', 'ec2', 'describe-instances', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for EC2 instances
        ec2_instances = aws_handler.collect_evidence(command_runner, aws_command_ec2_instances, output_file_ntp_config, return_data=True)

        for reservation in ec2_instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                output_file_instance_ntp = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.ec2_instance_{instance_id}_ntp.json"

                # Assuming SSM is used to manage NTP configurations
                aws_command_ssm = [
                    'aws', 'ssm', 'get-parameters', '--names', '/etc/ntp.conf', '--with-decryption', '--output', 'json'
                ]
                aws_handler.collect_evidence(command_runner, aws_command_ssm, output_file_instance_ntp)

        # Generate the output file path for CloudWatch Logs to check NTP synchronization logs
        output_file_cw_logs = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.cloudwatch_ntp_logs.json"

        # Define the AWS CLI command for describing CloudWatch log groups
        aws_command_cw_log_groups = [
            'aws', 'logs', 'describe-log-groups', '--log-group-name-prefix', '/aws/ntp/', '--output', 'json'
        ]

        # Collect evidence for CloudWatch log groups related to NTP
        cw_log_groups = aws_handler.collect_evidence(command_runner, aws_command_cw_log_groups, output_file_cw_logs, return_data=True)

        for log_group in cw_log_groups['logGroups']:
            log_group_name = log_group['logGroupName']
            output_file_log_streams = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.cloudwatch_ntp_log_streams_{log_group_name}.json"

            aws_command_log_streams = [
                'aws', 'logs', 'describe-log-streams', '--log-group-name', log_group_name, '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_log_streams, output_file_log_streams)

if __name__ == "__main__":
    main()
