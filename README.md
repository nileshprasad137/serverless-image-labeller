#### Serverless Image Labelling

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
