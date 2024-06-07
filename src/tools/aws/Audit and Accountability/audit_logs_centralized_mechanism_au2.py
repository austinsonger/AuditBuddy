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
    This script collects evidence of audit logs from the centralized auditing mechanism for each of the defined auditable events in AU-2.a.1 noting:
     - what type of event occurred
     - when the event occurred
     - where the event occurred
     - the source of the event
     - the outcome of the event
     - the identity of any individuals or subjects associated with the event

    Controls:
    - NIST 800-53 Requirement ID: AU-2 (Audit Events), AU-6 (Audit Review, Analysis, and Reporting)
    - SOC 2 Control Number: CC7.2 (Change Detection), CC7.3 (Incident Management)
    """
    command_runner = CommandRunner()

    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials

        aws_handler = AWSHandler(env_name, config)

        # Generate the output file path for CloudTrail event logs
        output_file_cloudtrail_logs = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.cloudtrail_audit_logs.json"

        # Define the AWS CLI command for describing CloudTrail events
        aws_command_cloudtrail_logs = [
            'aws', 'cloudtrail', 'lookup-events', '--region', config.region, '--output', 'json',
            '--start-time', '2023-01-01T00:00:00Z', '--end-time', current_date
        ]

        # Collect evidence for CloudTrail event logs
        cloudtrail_logs = aws_handler.collect_evidence(command_runner, aws_command_cloudtrail_logs, output_file_cloudtrail_logs, return_data=True)

        # Parse and store relevant details for each event
        parsed_events = []
        for event in cloudtrail_logs['Events']:
            event_details = {
                "EventType": event.get('EventName'),
                "EventTime": event.get('EventTime'),
                "EventSource": event.get('EventSource'),
                "AWSRegion": event.get('AwsRegion'),
                "SourceIPAddress": event.get('SourceIPAddress'),
                "UserIdentity": event.get('Username', event.get('UserIdentity', {}).get('Arn')),
                "EventOutcome": "Success" if event.get('ErrorCode') is None else f"Failed: {event.get('ErrorCode')}"
            }
            parsed_events.append(event_details)

        # Save parsed events to a JSON file
        parsed_output_file = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.parsed_audit_events.json"
        with open(parsed_output_file, 'w') as f:
            json.dump(parsed_events, f, indent=4)

if __name__ == "__main__":
    main()
