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

        # Generate the output file path for WAF rules
        waf_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.waf_rules_configuration.json"

        # Define the AWS CLI command for WAF rules
        waf_command = [
            'aws', 'waf', 'list-web-acls', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for WAF rules
        aws_handler.collect_evidence(command_runner, waf_command, waf_output_file)

        # Generate the output file path for firewall rules
        firewall_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.production_firewall_rules_configuration.json"

        # Define the AWS CLI command for firewall rules (assuming using Network Firewall)
        firewall_command = [
            'aws', 'network-firewall', 'describe-firewall', '--firewall-name', 'ProductionFirewall', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for firewall rules
        aws_handler.collect_evidence(command_runner, firewall_command, firewall_output_file)

        # Generate the output file path for security groups
        security_groups_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe_security_groups.json"

        # Define the AWS CLI command for security groups
        security_groups_command = [
            'aws', 'ec2', 'describe-security-groups', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for security groups
        aws_handler.collect_evidence(command_runner, security_groups_command, security_groups_output_file)

        # Generate the output file path for network ACLs
        network_acls_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.describe_network_acls.json"

        # Define the AWS CLI command for network ACLs
        network_acls_command = [
            'aws', 'ec2', 'describe-network-acls', '--region', config.region, '--output', 'json'
        ]

        # Collect evidence for network ACLs
        aws_handler.collect_evidence(command_runner, network_acls_command, network_acls_output_file)

if __name__ == "__main__":
    main()
