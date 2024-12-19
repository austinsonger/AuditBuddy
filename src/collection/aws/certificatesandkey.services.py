# Purpose: Provide Evidence for AWS Certificate & Key Management Related Services.#
###################################################################################
import os
import subprocess
import datetime
import json

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            # ACM Files
            'certificates': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificates.json",
            'certificate_details': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificate_details.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_tags.json",
            'renewal_status': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_renewal_status.json",
            # KMS Files
            'keys': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_keys.json",
            'key_policies': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_key_policies.json",
            'grants': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_grants.json",
            'kms_tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_tags.json"
        }
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            # ACM Files
            'certificates': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificates.json",
            'certificate_details': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificate_details.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_tags.json",
            'renewal_status': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_renewal_status.json",
            # KMS Files
            'keys': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_keys.json",
            'key_policies': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_key_policies.json",
            'grants': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_grants.json",
            'kms_tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_tags.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e}")
        return {}

# ACM Evidence Collection Functions
def fetch_certificates(config, output_file):
    certificates_data = run_command(['aws', 'acm', 'list-certificates', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(certificates_data, f, indent=4)

def fetch_certificate_details(config, output_file):
    certificates_data = run_command(['aws', 'acm', 'list-certificates', '--region', config['region'], '--output', 'json'])
    certificate_details_data = []
    for cert in certificates_data.get('CertificateSummaryList', []):
        cert_arn = cert['CertificateArn']
        cert_details = run_command(['aws', 'acm', 'describe-certificate', '--certificate-arn', cert_arn, '--output', 'json'])
        certificate_details_data.append(cert_details)
    with open(output_file, 'w') as f:
        json.dump(certificate_details_data, f, indent=4)

def fetch_acm_tags(config, output_file):
    certificates_data = run_command(['aws', 'acm', 'list-certificates', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for cert in certificates_data.get('CertificateSummaryList', []):
        cert_arn = cert['CertificateArn']
        cert_tags = run_command(['aws', 'acm', 'list-tags-for-certificate', '--certificate-arn', cert_arn, '--output', 'json'])
        tags_data.append({'CertificateArn': cert_arn, 'Tags': cert_tags.get('Tags', [])})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

def fetch_renewal_status(config, output_file):
    certificates_data = run_command(['aws', 'acm', 'list-certificates', '--region', config['region'], '--output', 'json'])
    renewal_status_data = []
    for cert in certificates_data.get('CertificateSummaryList', []):
        cert_arn = cert['CertificateArn']
        cert_renewal = run_command(['aws', 'acm', 'describe-certificate', '--certificate-arn', cert_arn, '--output', 'json'])
        renewal_status_data.append({
            'CertificateArn': cert_arn,
            'RenewalSummary': cert_renewal.get('RenewalSummary', {})
        })
    with open(output_file, 'w') as f:
        json.dump(renewal_status_data, f, indent=4)

# KMS Evidence Collection Functions
def fetch_keys(config, output_file):
    keys_data = run_command(['aws', 'kms', 'list-keys', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(keys_data, f, indent=4)

def fetch_key_policies(config, output_file):
    keys_data = run_command(['aws', 'kms', 'list-keys', '--region', config['region'], '--output', 'json'])
    key_policies_data = []
    for key in keys_data.get('Keys', []):
        key_id = key['KeyId']
        policy = run_command(['aws', 'kms', 'get-key-policy', '--key-id', key_id, '--policy-name', 'default', '--output', 'json'])
        key_policies_data.append({'KeyId': key_id, 'Policy': policy})
    with open(output_file, 'w') as f:
        json.dump(key_policies_data, f, indent=4)

def fetch_grants(config, output_file):
    keys_data = run_command(['aws', 'kms', 'list-keys', '--region', config['region'], '--output', 'json'])
    grants_data = []
    for key in keys_data.get('Keys', []):
        key_id = key['KeyId']
        key_grants = run_command(['aws', 'kms', 'list-grants', '--key-id', key_id, '--output', 'json'])
        recent_grants = [grant for grant in key_grants.get('Grants', []) if 'CreationDate' in grant and grant['CreationDate'] >= START_DATE]
        grants_data.extend(recent_grants)
    with open(output_file, 'w') as f:
        json.dump(grants_data, f, indent=4)

def fetch_kms_tags(config, output_file):
    keys_data = run_command(['aws', 'kms', 'list-keys', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for key in keys_data.get('Keys', []):
        key_id = key['KeyId']
        key_tags = run_command(['aws', 'kms', 'list-resource-tags', '--key-id', key_id, '--output', 'json'])
        tags_data.append({'KeyId': key_id, 'Tags': key_tags.get('Tags', [])})
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

        # Collect evidence for ACM configurations
        fetch_certificates(config, config['output_files']['certificates'])
        fetch_certificate_details(config, config['output_files']['certificate_details'])
        fetch_acm_tags(config, config['output_files']['tags'])
        fetch_renewal_status(config, config['output_files']['renewal_status'])

        # Collect evidence for KMS configurations
        fetch_keys(config, config['output_files']['keys'])
        fetch_key_policies(config, config['output_files']['key_policies'])
        fetch_grants(config, config['output_files']['grants'])
        fetch_kms_tags(config, config['output_files']['kms_tags'])

    print("AWS ACM and KMS configuration evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()
