# Purpose: Provide Evidence for AWS Container Related Services.#
################################################################
import os
import subprocess
import datetime
import json

YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'access_key': os.getenv('AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'output_files': {
            # ECS Files
            'clusters': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_clusters.json",
            'services': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_services.json",
            'tasks': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_tasks.json",
            'task_definitions': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_task_definitions.json",
            'ecs_tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_tags.json",
            # ECR Files
            'public_repositories': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_public_repositories.json",
            'public_images': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_public_images.json",
            'repository_policies': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_repository_policies.json",
            'ecr_tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_tags.json"
        }
    },
    'federal': {
        'access_key': os.getenv('DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-west-2',
        'output_files': {
            # ECS Files
            'clusters': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_clusters.json",
            'services': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_services.json",
            'tasks': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_tasks.json",
            'task_definitions': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_task_definitions.json",
            'ecs_tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecs_tags.json",
            # ECR Files
            'public_repositories': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_public_repositories.json",
            'public_images': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_public_images.json",
            'repository_policies': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_repository_policies.json",
            'ecr_tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-ecr_tags.json"
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

# ECS Evidence Collection Functions
def fetch_clusters(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(clusters_data, f, indent=4)

def fetch_services(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    services_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        services = run_command(['aws', 'ecs', 'list-services', '--cluster', cluster_arn, '--output', 'json'])
        services_data.extend(services.get('serviceArns', []))
    with open(output_file, 'w') as f:
        json.dump(services_data, f, indent=4)

def fetch_tasks(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    tasks_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        tasks = run_command(['aws', 'ecs', 'list-tasks', '--cluster', cluster_arn, '--output', 'json'])
        tasks_data.extend(tasks.get('taskArns', []))
    with open(output_file, 'w') as f:
        json.dump(tasks_data, f, indent=4)

def fetch_task_definitions(config, output_file):
    task_definitions_data = run_command(['aws', 'ecs', 'list-task-definitions', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(task_definitions_data, f, indent=4)

def fetch_ecs_tags(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        cluster_tags = run_command(['aws', 'ecs', 'list-tags-for-resource', '--resource-arn', cluster_arn, '--output', 'json'])
        tags_data.append({'ResourceArn': cluster_arn, 'Tags': cluster_tags.get('tags', [])})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# ECR Evidence Collection Functions
def fetch_public_repositories(config, output_file):
    public_repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(public_repositories_data, f, indent=4)

def fetch_public_images(config, output_file):
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    images_data = []
    for repo in repositories_data.get('repositories', []):
        repo_name = repo['repositoryName']
        images = run_command(['aws', 'ecr-public', 'describe-images', '--repository-name', repo_name, '--output', 'json'])
        images_data.extend(images.get('imageDetails', []))
    with open(output_file, 'w') as f:
        json.dump(images_data, f, indent=4)

def fetch_repository_policies(config, output_file):
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    repository_policies_data = []
    for repo in repositories_data.get('repositories', []):
        repo_name = repo['repositoryName']
        repo_policy = run_command(['aws', 'ecr-public', 'get-repository-policy', '--repository-name', repo_name, '--output', 'json'])
        repository_policies_data.append({'RepositoryName': repo_name, 'Policy': repo_policy})
    with open(output_file, 'w') as f:
        json.dump(repository_policies_data, f, indent=4)

def fetch_ecr_public_tags(config, output_file):
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for repo in repositories_data.get('repositories', []):
        repo_arn = repo['repositoryArn']
        repo_tags = run_command(['aws', 'ecr-public', 'list-tags-for-resource', '--resource-arn', repo_arn, '--output', 'json'])
        tags_data.append({'RepositoryArn': repo_arn, 'Tags': repo_tags.get('tags', [])})
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

        # Collect evidence for ECS configurations
        fetch_clusters(config, config['output_files']['clusters'])
        fetch_services(config, config['output_files']['services'])
        fetch_tasks(config, config['output_files']['tasks'])
        fetch_task_definitions(config, config['output_files']['task_definitions'])
        fetch_ecs_tags(config, config['output_files']['ecs_tags'])

        # Collect evidence for ECR configurations
        fetch_public_repositories(config, config['output_files']['public_repositories'])
        fetch_public_images(config, config['output_files']['public_images'])
        fetch_repository_policies(config, config['output_files']['repository_policies'])
        fetch_ecr_public_tags(config, config['output_files']['ecr_tags'])

    print("AWS ECS and ECR configuration evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()
