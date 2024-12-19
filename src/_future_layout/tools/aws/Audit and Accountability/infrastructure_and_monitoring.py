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

        # Infrastructure monitoring tool configuration of predefined rules for alerts
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.alert-rules.json"
        aws_command = [
            'aws', 'cloudwatch', 'describe-alarms', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

        # Servers have monitoring configuration enabled for events and metrics monitoring
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.server-monitoring.json"
        aws_command = [
            'aws', 'cloudwatch', 'describe-alarms', '--alarm-name-prefix', 'ServerMonitoring', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

        # Infrastructure monitoring metrics (CPU, storage, performance)
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.infrastructure-metrics.json"
        aws_command = [
            'aws', 'cloudwatch', 'get-metric-data', '--region', config.region, '--output', 'json',
            '--metric-data-queries', 'file://metric-queries.json'  # Assume metric-queries.json is pre-configured
        ]
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

        # Load balancers have access logs configuration enabled
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.elb-access-logs.json"
        aws_command = [
            'aws', 'elbv2', 'describe-load-balancer-attributes', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

        # Infrastructure monitoring tool dashboard report
        output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.monitoring-dashboard.json"
        aws_command = [
            'aws', 'cloudwatch', 'get-dashboard', '--dashboard-name', 'InfrastructureMonitoringDashboard', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command, output_file)

if __name__ == "__main__":
    main()
