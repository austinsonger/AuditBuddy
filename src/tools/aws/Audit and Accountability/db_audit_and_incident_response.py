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

        # Database audit trail logs rules configuration
        db_audit_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.db_audit_trail_logs.json"
        db_audit_command = [
            'aws', 'cloudtrail', 'lookup-events',
            '--lookup-attributes', 'AttributeKey=EventName,AttributeValue=ModifyDBInstance',
            '--region', config.region,
            '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, db_audit_command, db_audit_output_file)

        # Incident response tool configuration
        ir_tool_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.incident_response_tool_config.json"
        ir_tool_command = [
            'aws', 'cloudtrail', 'lookup-events',
            '--region',config.region,
            '--lookup-attributes', 'AttributeKey=EventName,AttributeValue=StopLogging',
            '--output', 'json'
        ]
        aws_handler.collect_evidence(command_runner, ir_tool_command, ir_tool_output_file)

if __name__ == "__main__":
    main()
