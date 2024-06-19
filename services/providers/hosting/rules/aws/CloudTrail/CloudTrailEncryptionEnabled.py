from aws_cdk import core
import boto3

class CloudTrailInfoRetrievalStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, info_function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Initialize a boto3 session
        session = boto3.Session()
        cloudtrail_client = session.client('cloudtrail')

        # Retrieve information about CloudTrails
        trails = cloudtrail_client.describe_trails()['trailList']

        # Loop through every CloudTrail and call the info_function
        for trail in trails:
            trail_name = trail['Name']
            info_function(cloudtrail_client, trail_name)

def check_cloudtrail_encryption(cloudtrail_client, trail_name):
    trail_status = cloudtrail_client.get_trail_status(Name=trail_name)
    encryption_enabled = trail_status.get('CloudTrailEncryptionEnabled', False)
    print(f"Trail {trail_name} encryption enabled: {encryption_enabled}")

app = core.App()

# Initialize stack with the encryption check function
CloudTrailInfoRetrievalStack(app, "CloudTrailInfoRetrievalStack", check_cloudtrail_encryption)

app.synth()
