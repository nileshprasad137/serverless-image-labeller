import json
import boto3
import os


def labelOnS3Upload(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    bucket = os.environ['SERVERLESS_IMAGE_LABELLING_BUCKET']
    region_name = os.environ['REGION_NAME']

    filesUploaded = event['Records']
    for file in filesUploaded:
        fileName = file["s3"]["object"]["key"]
        rekognitionClient = boto3.client('rekognition', region_name="us-east-1")
        response = rekognitionClient.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
            MaxLabels=10)
        print(response)

        print('Detected labels for ' + fileName)
        print()
        for label in response['Labels']:
            print ("Label: " + label['Name'])
            print ("Confidence: " + str(label['Confidence']))

        print(len(response['Labels']))

    finalResponse = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
#     print(finalResponse)
    return finalResponse

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
