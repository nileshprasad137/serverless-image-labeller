import json
import boto3
import os
import uuid


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
        rekognitionClient = boto3.client('rekognition', region_name=region_name)
        response = rekognitionClient.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
            MaxLabels=5)
        print(response)

        imageLabels = []
        print('Detected labels for ' + fileName)
        print()

        for label in response['Labels']:
            print ("Label: " + label['Name'])
            imageLabels.append(label["Name"])

    # Add to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    imageID = uuid.uuid1()
    addImageDataToMasterTableResponse = addImageDataToMasterTable(dynamodb=dynamodb, imageID=imageID, fileName=fileName,
                                                                  labels=imageLabels)
    print(json.dumps(addImageDataToMasterTableResponse))
    addToLabelMappingTableResponse = addToLabelMappingTable(dynamodb=dynamodb, imageID=imageID, fileName=fileName,
                                                                  labels=imageLabels)
    print(json.dumps(addToLabelMappingTableResponse))

    finalResponse = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    print(finalResponse)
    return finalResponse



def addImageDataToMasterTable(dynamodb, imageID, fileName, labels):
    masterImageTable = dynamodb.Table(os.environ['MASTER_IMAGE_TABLE'])
    item = {
                'imageID': str(imageID),
                'fileName': fileName,
                'labels': labels

    }

    # add image data to master MASTER_IMAGE_TABLE
    masterImageTable.put_item(Item=item)
    print("image data added to MASTER_IMAGE_TABLE")

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response

def addToLabelMappingTable(dynamodb, imageID, fileName, imageLabels):
    labelToS3MappingTable = dynamodb.Table(os.environ['LABEL_TO_S3_MAPPING_TABLE'])

    item = {
        'label': label,
        's3ImageFileNames': filename

    }

    # add to LABEL_TO_S3_MAPPING_TABLE
    labelToS3MappingTable.put_item(Item=item)
    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
    print("image data added to labelToS3MappingTable")

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
