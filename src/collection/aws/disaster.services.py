# Purpose: Provide Evidence for AWS Disaster Related Services.#
###############################################################
import os
import subprocess
import datetime
import json

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            'backup_vaults': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-backup_vaults.json",
            'backup_plans': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-backup_plans.json",
            'recovery_points': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-recovery_points.json",
            'tags': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-backup_tags.json"
        }
    },
    'federal': {
        'access_key': os.getenv('DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-west-2',
        'output_files': {
            'backup_vaults': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-backup_vaults.json",
            'backup_plans': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-backup_plans.json",
            'recovery_points': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-recovery_points.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-backup_tags.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Fetch all backup vaults and their configurations
def fetch_backup_vaults(config, output_file):
    vaults_data = run_command(['aws', 'backup', 'list-backup-vaults', '--region', config['region'], '--output', 'json'])
    detailed_vaults_data = []
    for vault in vaults_data['BackupVaultList']:
        vault_name = vault['BackupVaultName']
        vault_details = run_command(['aws', 'backup', 'describe-backup-vault', '--backup-vault-name', vault_name, '--output', 'json'])
        detailed_vaults_data.append(vault_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_vaults_data, f, indent=4)

# Fetch all backup plans and their configurations
def fetch_backup_plans(config, output_file):
    plans_data = run_command(['aws', 'backup', 'list-backup-plans', '--region', config['region'], '--output', 'json'])
    detailed_plans_data = []
    for plan in plans_data['BackupPlansList']:
        plan_id = plan['BackupPlanId']
        plan_details = run_command(['aws', 'backup', 'get-backup-plan', '--backup-plan-id', plan_id, '--output', 'json'])
        plan_rules = run_command(['aws', 'backup', 'list-backup-plan-versions', '--backup-plan-id', plan_id, '--output', 'json'])
        plan_details['BackupPlan']['Versions'] = plan_rules['BackupPlanVersionsList']
        detailed_plans_data.append(plan_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_plans_data, f, indent=4)

# Fetch all recovery points in each backup vault within the last 31 days
def fetch_recovery_points(config, output_file):
    vaults_data = run_command(['aws', 'backup', 'list-backup-vaults', '--region', config['region'], '--output', 'json'])
    recovery_points_data = []
    for vault in vaults_data['BackupVaultList']:
        vault_name = vault['BackupVaultName']
        recovery_points = run_command([
            'aws', 'backup', 'list-recovery-points-by-backup-vault',
            '--backup-vault-name', vault_name,
            '--by-created-after', START_DATE,
            '--by-created-before', END_DATE,
            '--output', 'json'
        ])
        for point in recovery_points.get('RecoveryPoints', []):
            point_arn = point['RecoveryPointArn']
            point_details = run_command(['aws', 'backup', 'describe-recovery-point', '--backup-vault-name', vault_name, '--recovery-point-arn', point_arn, '--output', 'json'])
            recovery_points_data.append(point_details)
    with open(output_file, 'w') as f:
        json.dump(recovery_points_data, f, indent=4)

# Fetch tags for each backup vault
def fetch_backup_tags(config, output_file):
    vaults_data = run_command(['aws', 'backup', 'list-backup-vaults', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for vault in vaults_data['BackupVaultList']:
        vault_arn = vault['BackupVaultArn']
        vault_tags = run_command(['aws', 'backup', 'list-tags', '--resource-arn', vault_arn, '--output', 'json'])
        tags_data.append({
            'BackupVaultArn': vault_arn,
            'Tags': vault_tags.get('Tags', {})
        })
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# Main function to execute each evidence collection task for both environments
def main():
    for env_name, config in environments.items():
        # Set AWS environment variables for each environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']
        
        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Collect evidence for AWS Backup configurations
        fetch_backup_vaults(config, config['output_files']['backup_vaults'])
        fetch_backup_plans(config, config['output_files']['backup_plans'])
        fetch_recovery_points(config, config['output_files']['recovery_points'])
        fetch_backup_tags(config, config['output_files']['tags'])

    print("AWS Backup configuration evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()
