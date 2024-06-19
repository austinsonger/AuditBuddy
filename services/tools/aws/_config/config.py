import os
from datetime import datetime, timezone

class EnvironmentConfig:
    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def set_aws_credentials(self):
        os.environ['AWS_ACCESS_KEY_ID'] = self.access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = self.secret_key
        os.environ['AWS_DEFAULT_REGION'] = self.region

current_year = datetime.now(timezone.utc).strftime('%Y')
current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

environments = {
    'private-sector': EnvironmentConfig(
        access_key=os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        secret_key=os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        region='us-east-1'
    ),
    'federal': EnvironmentConfig(
        access_key=os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        secret_key=os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        region='us-east-1'
    )
}
