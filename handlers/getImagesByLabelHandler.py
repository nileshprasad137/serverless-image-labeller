import json
import boto3
import os
import uuid

def getImagesByLabel(event, context):
    bucket = os.environ['SERVERLESS_IMAGE_LABELLING_BUCKET']
    region_name = os.environ['REGION_NAME']
    requestBody = json.loads(event["body"])
    print(requestBody)
    requestLabel = requestBody["label"].lower()
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    imageIDResponse = getImageID(dynamodb=dynamodb, requestLabel=requestLabel)
    print (imageIDResponse)
    imageSet = set(imageIDResponse["Item"]["imageIDs"])
    print (imageSet)

    results = []
    for image in imageSet:
        result = getImageDetails(dynamodb=dynamodb,imageID=image)["Item"]
        results.append(result)

    imageDetailResponse = {
        "Images" : results
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(imageDetailResponse)
    }

    return response

def getImageID(dynamodb, requestLabel):
    labelToS3MappingTable = dynamodb.Table(os.environ['LABEL_TO_S3_MAPPING_TABLE'])

    imageData = labelToS3MappingTable.get_item(
        Key={
            'label': requestLabel
        }
    )

    return imageData

def getImageDetails(dynamodb, imageID):
    masterImageTable = dynamodb.Table(os.environ['MASTER_IMAGE_TABLE'])

    imageData = masterImageTable.get_item(
        Key={
            'imageID': imageID
        }
    )

    return imageData

