# main.py
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

        # Define the evidence description
        evidence_description = "database_backup_configurations"

        # Generate the output file paths
        output_file_rds_snapshots = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_rds_snapshots.json"
        output_file_backup_vaults = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_backup_vaults.json"
        output_file_backup_plans = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_backup_plans.json"

        # Define the AWS CLI commands with output file paths
        aws_command_rds_snapshots = [
            'aws', 'rds', 'describe-db-snapshots', '--region', config.region, '--output', 'json'
        ]
        aws_command_backup_vaults = [
            'aws', 'backup', 'list-backup-vaults', '--region', config.region, '--output', 'json'
        ]
        aws_command_backup_plans = [
            'aws', 'backup', 'list-backup-plans', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_rds_snapshots, output_file_rds_snapshots)
        aws_handler.collect_evidence(command_runner, aws_command_backup_vaults, output_file_backup_vaults)
        aws_handler.collect_evidence(command_runner, aws_command_backup_plans, output_file_backup_plans)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- CP-9: Contingency Planning / Information System Backup
- CP-10: Contingency Planning / Information System Recovery and Reconstitution

SOC 2 Control Numbers:
- CC7.2: Change Management
- CC7.3: Availability
"""
