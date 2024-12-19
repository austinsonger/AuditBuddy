# main.py
import sys
import os
import json

# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

"""
Description: This script collects evidence of the certificate authority for the information system
responsible for establishing and managing cryptographic keys. It does so by checking the configurations
of AWS Certificate Manager (ACM) and AWS CloudHSM, and saves the evidence in a JSON file named with
the current date and environment name.
"""

def main():
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.certificate_authority.json"

        # Define the AWS CLI command to list all certificates
        list_certificates_command = [
            'aws', 'acm', 'list-certificates',
            '--region', config.region, '--output', 'json'
        ]

        # Run the command to list all certificates
        certificates_output = command_runner.run_command(list_certificates_command)
        certificates = json.loads(certificates_output).get('CertificateSummaryList', [])

        # Initialize a list to hold detailed certificate information
        detailed_certificates_info = []

        # Loop through each certificate ARN and describe the certificate
        for certificate in certificates:
            certificate_arn = certificate['CertificateArn']
            describe_certificate_command = [
                'aws', 'acm', 'describe-certificate',
                '--certificate-arn', certificate_arn,
                '--region', config.region, '--output', 'json'
            ]
            certificate_info = command_runner.run_command(describe_certificate_command)
            detailed_certificates_info.append(json.loads(certificate_info))

        # Collect CloudHSM cluster information
        describe_clusters_command = [
            'aws', 'cloudhsm', 'describe-clusters',
            '--region', config.region, '--output', 'json'
        ]
        clusters_info = command_runner.run_command(describe_clusters_command)

        # Combine all the evidence
        evidence = {
            "Certificates": detailed_certificates_info,
            "CloudHSMClusters": json.loads(clusters_info)
        }

        # Save the combined evidence to the output file
        with open(output_file, 'w') as f:
            json.dump(evidence, f, indent=4)

if __name__ == "__main__":
    main()
