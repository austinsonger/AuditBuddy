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
    This script collects evidence of configurations to prevent the installation of software/firmware without verification that such components have been digitally signed and approved by the organization by querying various AWS services.

    Controls:
    - NIST 800-53 Requirement ID: SA-12 (Supply Chain Protection), CM-5 (Access Restrictions for Change)
    - SOC 2 Control Number: CC6.6 (Change Management)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for IAM policies related to code signing
        output_file_iam_policies = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.iam_policies_code_signing.json"

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

        # Generate the output file path for S3 bucket policies related to software repositories
        output_file_s3_policies = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.s3_bucket_policies_software_repos.json"

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

        # Generate the output file path for AWS CodePipeline configurations
        output_file_codepipeline = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.codepipeline_configurations.json"

        # Define the AWS CLI command for listing CodePipeline pipelines
        aws_command_codepipeline = [
            'aws', 'codepipeline', 'list-pipelines', '--output', 'json'
        ]

        # Collect evidence for CodePipeline configurations
        pipelines = aws_handler.collect_evidence(command_runner, aws_command_codepipeline, output_file_codepipeline, return_data=True)
        for pipeline in pipelines['pipelines']:
            pipeline_name = pipeline['name']
            output_file_pipeline_details = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.codepipeline_{pipeline_name}_details.json"
            aws_command_pipeline_details = [
                'aws', 'codepipeline', 'get-pipeline', '--name', pipeline_name, '--output', 'json'
            ]
            aws_handler.collect_evidence(command_runner, aws_command_pipeline_details, output_file_pipeline_details)

if __name__ == "__main__":
    main()
