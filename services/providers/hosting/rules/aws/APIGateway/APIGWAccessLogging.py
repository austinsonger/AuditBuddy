from aws_cdk import core
import boto3

class APIGatewayInfoRetrievalStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, info_function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Initialize a boto3 session
        session = boto3.Session()
        apigw_client = session.client('apigateway')

        # Retrieve information about API Gateway rest APIs
        rest_apis = apigw_client.get_rest_apis()['items']

        # Loop through each API Gateway and call the info_function
        for rest_api in rest_apis:
            api_id = rest_api['id']
            stages = apigw_client.get_stages(restApiId=api_id)['item']
            for stage in stages:
                stage_name = stage['stageName']
                info_function(apigw_client, api_id, stage_name)

def check_apigw_access_logging(apigw_client, api_id, stage_name):
    stage = apigw_client.get_stage(restApiId=api_id, stageName=stage_name)
    access_logging_enabled = 'accessLogSettings' in stage and stage['accessLogSettings'].get('destinationArn')
    print(f"API ID: {api_id}, Stage: {stage_name}, Access Logging Enabled: {access_logging_enabled}")

app = core.App()

# Initialize stack with the access logging check function
APIGatewayInfoRetrievalStack(app, "APIGatewayInfoRetrievalStack", check_apigw_access_logging)

app.synth()
