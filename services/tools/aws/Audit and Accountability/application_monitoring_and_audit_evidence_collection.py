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

        # Evidence 1: Application monitoring tool dashboard report proving existence of a dedicated tool
        output_file_1 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.application_monitoring_tool_dashboard_report.json"
        aws_command_1 = [
            'aws', 'cloudwatch', 'describe-alarms', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command_1, output_file_1)

        # Evidence 2: Application monitoring tools configuration showing alert rules for anomaly detection
        output_file_2 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.application_monitoring_tools_configuration.json"
        aws_command_2 = [
            'aws', 'cloudwatch', 'describe-anomaly-detectors', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command_2, output_file_2)

        # Evidence 3: User audit trail activity configuration of environment's services and resources
        output_file_3 = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.user_audit_trail_activity_configuration.json"
        aws_command_3 = [
            'aws', 'cloudtrail', 'describe-trails', '--region', config.region, '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, aws_command_3, output_file_3)

if __name__ == "__main__":
    main()
