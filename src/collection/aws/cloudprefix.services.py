# Purpose: Provide Evidence for AWS Cloud**** Related Services.#
################################################################
import os
import subprocess
import datetime
import json


YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.utcnow().isoformat()

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            # CloudWatch Files
            'alarms': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_alarms.json",
            'metrics': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_metrics.json",
            'dashboards': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_dashboards.json",
            'log_groups': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_log_groups.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_tags.json",
            # CloudTrail Files
            'trails': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_trails.json",
            'event_data_stores': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_event_data_stores.json",
            'insights': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_insights.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_tags.json"
        }
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-west-2',
        'output_files': {
            # CloudWatch Files
            'alarms': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_alarms.json",
            'metrics': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_metrics.json",
            'dashboards': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_dashboards.json",
            'log_groups': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_log_groups.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_tags.json",
            # CloudTrail Files
            'trails': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_trails.json",
            'event_data_stores': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_event_data_stores.json",
            'insights': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_insights.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_tags.json"
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

# CloudWatch Evidence Collection Functions
def fetch_alarms(config, output_file):
    alarms_data = run_command(['aws', 'cloudwatch', 'describe-alarms', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(alarms_data, f, indent=4)

def fetch_metrics(config, output_file):
    metrics_data = run_command(['aws', 'cloudwatch', 'list-metrics', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(metrics_data, f, indent=4)

def fetch_dashboards(config, output_file):
    dashboards_data = run_command(['aws', 'cloudwatch', 'list-dashboards', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(dashboards_data, f, indent=4)

def fetch_log_groups(config, output_file):
    log_groups_data = run_command(['aws', 'logs', 'describe-log-groups', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(log_groups_data, f, indent=4)

def fetch_cloudwatch_tags(config, output_file):
    log_groups_data = run_command(['aws', 'logs', 'describe-log-groups', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for log_group in log_groups_data.get('logGroups', []):
        log_group_name = log_group['logGroupName']
        tags = run_command(['aws', 'logs', 'list-tags-log-group', '--log-group-name', log_group_name, '--output', 'json'])
        tags_data.append({'LogGroupName': log_group_name, 'Tags': tags.get('tags', {})})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# CloudTrail Evidence Collection Functions
def fetch_trails(config, output_file):
    trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(trails_data, f, indent=4)

def fetch_event_data_stores(config, output_file):
    event_data_stores_data = run_command(['aws', 'cloudtrail', 'list-event-data-stores', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(event_data_stores_data, f, indent=4)

def fetch_insights_selectors(config, output_file):
    trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
    insights_data = []
    for trail in trails_data['Trails']:
        trail_name = trail['Name']
        insights_selectors = run_command(['aws', 'cloudtrail', 'get-insight-selectors', '--trail-name', trail_name, '--output', 'json'])
        insights_data.append({
            'TrailName': trail_name,
            'InsightSelectors': insights_selectors.get('InsightSelectors', [])
        })
    with open(output_file, 'w') as f:
        json.dump(insights_data, f, indent=4)

def fetch_cloudtrail_tags(config, output_file):
    trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for trail in trails_data['Trails']:
        trail_arn = trail['TrailARN']
        trail_tags = run_command(['aws', 'cloudtrail', 'list-tags', '--resource-id-list', trail_arn, '--output', 'json'])
        tags_data.append({
            'TrailARN': trail_arn,
            'Tags': trail_tags.get('ResourceTagList', [])
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

        # Collect evidence for AWS CloudWatch configurations
        fetch_alarms(config, config['output_files']['alarms'])
        fetch_metrics(config, config['output_files']['metrics'])
        fetch_dashboards(config, config['output_files']['dashboards'])
        fetch_log_groups(config, config['output_files']['log_groups'])
        fetch_cloudwatch_tags(config, config['output_files']['tags'])

        # Collect evidence for AWS CloudTrail configurations
        fetch_trails(config, config['output_files']['trails'])
        fetch_event_data_stores(config, config['output_files']['event_data_stores'])
        fetch_insights_selectors(config, config['output_files']['insights'])
        fetch_cloudtrail_tags(config, config['output_files']['tags'])

    print("AWS CloudWatch and CloudTrail configuration evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()
