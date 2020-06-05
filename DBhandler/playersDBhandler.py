import json
import boto3

def get_players(event, context):
    method = event['httpMethod']
    path = event['path']
        
    if (method == 'POST'):
        body = json.loads(event['body'])
        id = body["id"]
        name = body["name"]
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Hello, CDK! You have hit POST id and name: {} {}\n'.format(id, name)
            }

def get_player(event, context):

def add_player(event, context):

def update_player(event, context):

def delete_player(event, context):
