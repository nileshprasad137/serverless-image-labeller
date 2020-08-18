
#### Serverless Image Labelling

<img src="https://user-images.githubusercontent.com/16336390/90423966-fb30e780-e0da-11ea-8adf-01124ca0bfc3.png" width="600" height="500" />

#### Use-Cases

Storing images in S3 Bucket with label information. **AWS Rekognition** is used for detecting labels in image. You can later query the API endpoint provided by this serverless service to get the list of images which belongs to particular label. 

On deploying, this provisions 2 Lambda functions in your AWS setup. One Lambda function is responsible to store the image labels on each successful PUT operation in specified S3 bucket. The other Lambda function is used to retrieve the images of a particular label.

#### Usage

This project uses `serverless` framework. So, make sure you get that first and give the necessary permissions to `serverless cli`. Follow [this page](https://www.serverless.com/framework/docs/getting-started/) for getting started. <br>
Before `sls deploy`, make sure you have setup these resources in AWS.
```
aws dynamodb create-table --cli-input-json file://setup/create-label-to-s3-mapping-table.json --region us-east-1
aws dynamodb create-table --cli-input-json file://setup/create-master-image-label-table.json --region us-east-1
aws s3 mb s3://serverless-image-labelling-bucket --region=us-east-1
```

```
# Install the necessary plugin
$ sls plugin install -n serverless-python-requirements
```
```
# Deploy to AWS
$ sls deploy
```
After deployment is successful, you can check the setup details using `sls info` . Now, you can test the services by uploading an image on **S3.** This would label the image and store the details in **DyanamoDB**. You can later query the endpoint for getting images associated to the label.

Example,

    curl -X POST \
      https://xxxxxxxxxxxx.amazonaws.com/dev/getImagesByLabel \
      -H 'Content-Type: application/json' \
      -H 'Postman-Token: f769a23f-d285-4aba-9fc1-f3d8dd4b9f33' \
      -H 'cache-control: no-cache' \
      -d '{"label":"Furniture"}'
      
####### Featured as community example for Serverless framework.


