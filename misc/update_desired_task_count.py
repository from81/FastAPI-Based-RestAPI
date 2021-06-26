import datetime

import boto3
import json

client = boto3.client('ecs')

def datetime_converter(dt):
    if isinstance(dt, datetime.datetime):
        return dt.__str__()

def lambda_handler(event, context):
    print("Received event: \n" + json.dumps(event, indent=4))
    
    body = json.loads(event["body"])
    n = body["taskCount"]
    
    if type(n) != int:
        n = int(n)
        
    try:
        response = client.update_service(cluster='geoapi-cluster', service='geoapi', desiredCount=n, forceNewDeployment=True)
        return {
            'statusCode': 200,
            'body': json.dumps(response, default=datetime_converter, indent=4)
        }
    except Exception as e:
        print(e)
        raise e