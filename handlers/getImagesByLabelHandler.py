import json
import boto3
import os
import uuid

def getImagesByLabel(event, context):
    bucket = os.environ['SERVERLESS_IMAGE_LABELLING_BUCKET']
    region_name = os.environ['REGION_NAME']

    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }

    print(response)
    return response