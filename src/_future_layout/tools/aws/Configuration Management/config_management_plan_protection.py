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
    This script collects evidence of protection mechanisms for the configuration management plan from unauthorized disclosure and modification by querying various AWS services.

    Controls:
    - NIST 800-53 Requirement ID: CM-9 (Configuration Management Plan), SC-28 (Protection of Information at Rest)
    - SOC 2 Control Number: CC6.1 (Logical and Physical Access Controls), CC6.3 (Change Management)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for IAM policies related to configuration management
        output_file_iam_policies = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.iam_policies_configuration_management.json"

        # Define the AWS CLI command for listing IAM policies
        aws_command_iam_policies = [
            'aws', 'iam', 'list-policies', '--output', 'json'
        ]

        # Collect evidence for IAM policies
        iam_policies = aws_handler.collect_evidence(command_runner, aws_command_iam_policies, output_file_iam_policies, return_data=True)
        for policy in iam_policies['Policies']:
            policy_arn = policy['Arn']
            output_file_iam_policy_version = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.iam_policy_{policy_arn}_version.json"
            aws_command_iam_policy_version = [
                'aws', 'iam', 'get-policy-version', '--policy-arn', policy_arn, '--version-id', policy['DefaultVersionId'], '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_iam_policy_version, output_file_iam_policy_version)

        # Generate the output file path for S3 bucket policies related to configuration management plans
        output_file_s3_policies = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.s3_bucket_policies_configuration_management.json"

        # Define the AWS CLI command for listing S3 buckets
        aws_command_s3_buckets = [
            'aws', 's3api', 'list-buckets', '--query', 'Buckets[*].Name', '--output', 'json'
        ]

        # Collect evidence for S3 bucket policies
        s3_buckets = aws_handler.collect_evidence(command_runner, aws_command_s3_buckets, output_file_s3_policies, return_data=True)
        for bucket in s3_buckets:
            output_file_s3_bucket_policy = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.s3_bucket_{bucket}_policy.json"
            aws_command_s3_bucket_policy = [
                'aws', 's3api', 'get-bucket-policy', '--bucket', bucket, '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_s3_bucket_policy, output_file_s3_bucket_policy)

        # Generate the output file path for CloudTrail configurations to ensure logging and monitoring
        output_file_cloudtrail = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.cloudtrail_configurations.json"

        # Define the AWS CLI command for describing CloudTrail trails
        aws_command_cloudtrail = [
            'aws', 'cloudtrail', 'describe-trails', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for CloudTrail configurations
        aws_handler.collect_evidence(command_runner, aws_command_cloudtrail, output_file_cloudtrail)

        # Generate the output file path for Config rules to ensure compliance and security configurations
        output_file_config_rules = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.config_rules.json"

        # Define the AWS CLI command for describing AWS Config rules
        aws_command_config_rules = [
            'aws', 'configservice', 'describe-config-rules', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for AWS Config rules
        aws_handler.collect_evidence(command_runner, aws_command_config_rules, output_file_config_rules)

if __name__ == "__main__":
    main()
