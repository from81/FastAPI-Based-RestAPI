
start local dynamodb instance:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`

check if dynamo is running:
`aws dynamodb list-tables --endpoint-url http://localhost:8000`
