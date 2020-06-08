import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("TABLE_PLAYERS"))

def get_players(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        items = table.scan()["Items"]
    return {
        "body": json.dumps(items, indent=2, sort_keys=True),
        "statusCode": 200
    }

def get_player(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        id = event['pathParameters']['player_id']
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

def add_player(event, context):
    method = event['httpMethod']
    if (method == 'POST'):
        body = json.loads(event['body'])
        item = {
                'id' : str(uuid.uuid4()),
                'login': body['login'],
                'first_name': body['first_name'],
                'last_name': body['last_name'],
                'birth_date': body['birth_date'],
                'team': body['team'],
            }
        table.put_item(
            Item=item
        )
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Item created: {}'.format(str(json.dumps(item, indent=2, sort_keys=True)))
            }

# def update_player(event, context):
#     method = event['httpMethod']
#     if (method == 'PUT'):
#         id = event['pathParameters']['player_id']
#         body = json.loads(event['body'])
#         item = {
#                 'id' : str(uuid.uuid4()),
#                 'login': body['login'],
#                 'first_name': body['first_name'],
#                 'last_name': body['last_name'],
#                 'birth_date': body['birth_date'],
#                 'team': body['team'],
#             }
#         table.put_item(
#             Item=item
#         )
#         return {
#             'statusCode': 200,
#             'headers': {
#             'Content-Type': 'text/plain'
#                 },
#                 'body': 'Item updated: {}'.format(str(json.dumps(item, indent=2, sort_keys=True)))
#             }

def delete_player(event, context):
    method = event['httpMethod']
    if (method == 'DELETE'):
        id = event['pathParameters']['player_id']
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
