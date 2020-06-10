import json
import boto3
import os
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
#s3client = boto3.client("s3")

#enviroment variables
table = dynamodb.Table(os.getenv("TABLE_TEAMS"))
bucket = os.getenv("BUCKET")

def get_teams(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        items = table.scan()["Items"]
        return {
            "body": json.dumps(items, indent=2, sort_keys=True),
            "statusCode": 200
        }

def get_team(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        id = event['pathParameters']['team_id']
        item = table.get_item(
            Key ={
                "id" : id
            }
        )
        item = item['Item']
        return {
        "body": json.dumps(item, indent=2, sort_keys=True),
        "statusCode": 200
        }

def add_team(event, context):
    method = event['httpMethod']
    if (method == 'POST'):
        id = str(uuid.uuid4())
        body = json.loads(event['body'])
        item = {
                'id' : id,
                'name': body['name'],
            }
        table.put_item(
            Item=item
        )
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Item created: {}'.format(json.dumps(item, indent=2, sort_keys=True))
            }

#def update_team:
    #TO-DO

def delete_team(event, context):
    method = event['httpMethod']
    if (method == 'DELETE'):
        id = event['pathParameters']['team_id']
        table.delete_item(
            Key={
                "id" : id
            }
        )
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Item deleted: {}'.format(str(id))
            }
