#### Serverless Image Labelling

<img src="https://user-images.githubusercontent.com/16336390/90423966-fb30e780-e0da-11ea-8adf-01124ca0bfc3.png" width="600" height="500" />

```

aws dynamodb create-table --cli-input-json file://setup/create-label-to-s3-mapping-table.json --region us-east-1

aws dynamodb create-table --cli-input-json file://setup/create-master-image-label-table.json --region us-east-1


aws dynamodb list-tables --region=us-east-1

aws s3 mb s3://serverless-image-labelling-bucket --region=us-east-1

aws dynamodb update-item --table-name users \
--key '{"userId": {"S": "my-user-id"}}' \ 
--update-expression "ADD friends :friends" \
--expression-attribute-values '{":friends": {"SS": ["friend1-id", "friend2-id"]}}'
```
