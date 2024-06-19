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
    This script collects evidence of security measures for the protection of development, testing, and production environments for software development by querying various AWS services.

    Controls:
    - NIST 800-53 Requirement ID: SC-7 (Boundary Protection), CM-2 (Baseline Configuration), CM-6 (Configuration Settings)
    - SOC 2 Control Number: CC6.1 (Logical and Physical Access Controls), CC6.2 (System Component Identification)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for EC2 security groups
        output_file_sg = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.security_groups.json"

        # Define the AWS CLI command for describing EC2 security groups
        aws_command_sg = [
            'aws', 'ec2', 'describe-security-groups', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for EC2 security groups
        aws_handler.collect_evidence(command_runner, aws_command_sg, output_file_sg)

        # Generate the output file path for IAM roles and policies
        output_file_iam = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.iam_roles_policies.json"

        # Define the AWS CLI command for listing IAM roles
        aws_command_iam_roles = [
            'aws', 'iam', 'list-roles', '--output', 'json'
        ]

        # Collect evidence for IAM roles
        iam_roles = aws_handler.collect_evidence(command_runner, aws_command_iam_roles, output_file_iam, return_data=True)
        for role in iam_roles['Roles']:
            role_name = role['RoleName']
            output_file_iam_role_policy = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.iam_role_{role_name}_policies.json"
            aws_command_iam_role_policy = [
                'aws', 'iam', 'list-role-policies', '--role-name', role_name, '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_iam_role_policy, output_file_iam_role_policy)

        # Generate the output file path for CloudTrail configurations
        output_file_cloudtrail = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.cloudtrail_configurations.json"

        # Define the AWS CLI command for describing CloudTrail trails
        aws_command_cloudtrail = [
            'aws', 'cloudtrail', 'describe-trails', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for CloudTrail configurations
        aws_handler.collect_evidence(command_runner, aws_command_cloudtrail, output_file_cloudtrail)

        # Generate the output file path for Config rules
        output_file_config_rules = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.config_rules.json"

        # Define the AWS CLI command for describing AWS Config rules
        aws_command_config_rules = [
            'aws', 'configservice', 'describe-config-rules', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for AWS Config rules
        aws_handler.collect_evidence(command_runner, aws_command_config_rules, output_file_config_rules)

if __name__ == "__main__":
    main()
