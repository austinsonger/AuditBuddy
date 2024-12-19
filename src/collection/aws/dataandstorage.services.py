# Purpose: Provide Evidence for AWS Data & Storage Related Services.#
#####################################################################
import os
import subprocess
import datetime
import json


# Define current year, month, and day for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.utcnow().isoformat()

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            'db_instances': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_instances.json',
            'db_snapshots': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_snapshots.json',
            'db_clusters': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_clusters.json',
            'db_security_groups': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_security_groups.json',
            'db_subnet_groups': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_subnet_groups.json',
            'db_log_files': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-db_log_files.json',
            'certificates': f'/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-certificates.json'
            'ebs_volumes': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_volumes.json',
            'ebs_snapshots': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_file_systems.json',
            'efs_lifecycle_policies': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_lifecycle_policies.json',
            'efs_access_points': f'/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_access_points.json',
        }
    },
    'federal': {
        'access_key': os.getenv('DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-west-2',
        'output_files': {
            'db_instances': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_instances.json',
            'db_snapshots': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_snapshots.json',
            'db_clusters': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_clusters.json',
            'db_security_groups': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_security_groups.json',
            'db_subnet_groups': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_subnet_groups.json',
            'db_log_files': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-db_log_files.json',
            'certificates': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-certificates.json'
            'ebs_volumes': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_volumes.json',
            'ebs_snapshots': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_file_systems.json',
            'efs_lifecycle_policies': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_lifecycle_policies.json',
            'efs_access_points': f'/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-efs_access_points.json',
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Function to fetch all DB instances and their details
def fetch_db_instances(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-db-instances', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_instance in list_data['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-instances', '--db-instance-identifier', db_instance_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB snapshots and their details
def fetch_db_snapshots(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-db-snapshots', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for snapshot in list_data['DBSnapshots']:
        snapshot_id = snapshot['DBSnapshotIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-snapshots', '--db-snapshot-identifier', snapshot_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB clusters and their details
def fetch_db_clusters(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-db-clusters', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_cluster in list_data.get('DBClusters', []):
        db_cluster_id = db_cluster['DBClusterIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-clusters', '--db-cluster-identifier', db_cluster_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB security groups and their details
def fetch_db_security_groups(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-db-security-groups', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_sg in list_data.get('DBSecurityGroups', []):
        db_sg_name = db_sg['DBSecurityGroupName']
        details = run_command(['aws', 'rds', 'describe-db-security-groups', '--db-security-group-name', db_sg_name, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB subnet groups and their details
def fetch_db_subnet_groups(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-db-subnet-groups', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(list_data['DBSubnetGroups'], f, indent=4)

# Function to fetch DB log files for each DB instance
def fetch_db_log_files(config, output_file):
    db_instances = run_command(['aws', 'rds', 'describe-db-instances', '--region', config['region'], '--output', 'json'])
    log_files_data = {}
    for db_instance in db_instances['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        logs = run_command(['aws', 'rds', 'describe-db-log-files', '--db-instance-identifier', db_instance_id, '--output', 'json'])
        log_files_data[db_instance_id] = logs.get('DescribeDBLogFiles', [])
    with open(output_file, 'w') as f:
        json.dump(log_files_data, f, indent=4)

# Function to fetch all certificates and their details
def fetch_certificates(config, output_file):
    list_data = run_command(['aws', 'rds', 'describe-certificates', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(list_data['Certificates'], f, indent=4)

# EBS Functions
def fetch_ebs_volumes(config, output_file):
    print("Fetching EBS volumes...")
    volumes = run_command(['aws', 'ec2', 'describe-volumes', '--region', config['region'], '--output', 'json'])
    detailed_volumes = []
    for volume in volumes.get('Volumes', []):
        volume_id = volume['VolumeId']
        details = run_command(['aws', 'ec2', 'describe-volumes', '--volume-ids', volume_id, '--region', config['region'], '--output', 'json'])
        detailed_volumes.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_volumes, f, indent=4)

def fetch_ebs_snapshots(config, output_file):
    print("Fetching EBS snapshots...")
    snapshots = run_command(['aws', 'ec2', 'describe-snapshots', '--owner-ids', 'self', '--region', config['region'], '--output', 'json'])
    detailed_snapshots = []
    for snapshot in snapshots.get('Snapshots', []):
        snapshot_id = snapshot['SnapshotId']
        details = run_command(['aws', 'ec2', 'describe-snapshots', '--snapshot-ids', snapshot_id, '--region', config['region'], '--output', 'json'])
        detailed_snapshots.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_snapshots, f, indent=4)

def fetch_ebs_lifecycle_policies(config, output_file):
    print("Fetching EBS lifecycle policies...")
    policies = run_command(['aws', 'dlm', 'get-lifecycle-policies', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(policies, f, indent=4)

# EFS Functions
def fetch_efs_file_systems(config, output_file):
    print("Fetching EFS file systems...")
    file_systems = run_command(['aws', 'efs', 'describe-file-systems', '--region', config['region'], '--output', 'json'])
    detailed_file_systems = []
    for fs in file_systems.get('FileSystems', []):
        fs_id = fs['FileSystemId']
        details = run_command(['aws', 'efs', 'describe-file-systems', '--file-system-id', fs_id, '--region', config['region'], '--output', 'json'])
        detailed_file_systems.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_file_systems, f, indent=4)

def fetch_efs_lifecycle_policies(config, output_file):
    print("Fetching EFS lifecycle policies...")
    file_systems = run_command(['aws', 'efs', 'describe-file-systems', '--region', config['region'], '--output', 'json'])
    lifecycle_policies = []
    for fs in file_systems.get('FileSystems', []):
        fs_id = fs['FileSystemId']
        policy = run_command(['aws', 'efs', 'describe-lifecycle-configuration', '--file-system-id', fs_id, '--region', config['region'], '--output', 'json'])
        lifecycle_policies.append({'FileSystemId': fs_id, 'LifecycleConfiguration': policy})
    with open(output_file, 'w') as f:
        json.dump(lifecycle_policies, f, indent=4)

def fetch_efs_access_points(config, output_file):
    print("Fetching EFS access points...")
    access_points = run_command(['aws', 'efs', 'describe-access-points', '--region', config['region'], '--output', 'json'])
    detailed_access_points = []
    for ap in access_points.get('AccessPoints', []):
        ap_id = ap['AccessPointId']
        details = run_command(['aws', 'efs', 'describe-access-points', '--access-point-id', ap_id, '--region', config['region'], '--output', 'json'])
        detailed_access_points.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_access_points, f, indent=4)

# Main function to execute each evidence collection task
def main():
    for env_name, config in environments.items():
        # Set AWS environment variables for each environment
        os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']
        
        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Collect evidence for each RDS configuration type
        fetch_db_instances(config, config['output_files']['db_instances'])
        fetch_db_snapshots(config, config['output_files']['db_snapshots'])
        fetch_db_clusters(config, config['output_files']['db_clusters'])
        fetch_db_security_groups(config, config['output_files']['db_security_groups'])
        fetch_db_subnet_groups(config, config['output_files']['db_subnet_groups'])
        fetch_db_log_files(config, config['output_files']['db_log_files'])
        fetch_certificates(config, config['output_files']['certificates'])

        # Collect evidence for EBS configurations
        fetch_ebs_volumes(config, config['output_files']['ebs_volumes'])
        fetch_ebs_snapshots(config, config['output_files']['ebs_snapshots'])
        fetch_ebs_lifecycle_policies(config, config['output_files']['ebs_lifecycle_policies'])

        # Collect evidence for EFS configurations
        fetch_efs_file_systems(config, config['output_files']['efs_file_systems'])
        fetch_efs_lifecycle_policies(config, config['output_files']['efs_lifecycle_policies'])
        fetch_efs_access_points(config, config['output_files']['efs_access_points'])

    
    print("Evidence collection completed.")

# Execute main function
if __name__ == "__main__":
    main()
