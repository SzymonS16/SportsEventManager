import json
import boto3
import os
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')
s3client = boto3.client("s3")

table = dynamodb.Table(os.getenv("TABLE_SPORT_FACILITIES"))
queue = sqs.Queue(os.getenv("QUEUE_FACILITIES_URL"))
bucket = os.getenv("BUCKET")

def get_sport_facilities(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        items = table.scan()["Items"]
        return {
            "body": json.dumps(items, indent=2, sort_keys=True),
            "statusCode": 200
        }

def get_sport_facility(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        id = event['pathParameters']['facility_id']
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

def add_sport_facility(event, context):
    method = event['httpMethod']
    if (method == 'POST'):
        id = str(uuid.uuid4())
        body = json.loads(event['body'])
        item = {
                'id' : id,
                'name': body['name'],
                'type' : body['type']
            }
        
        response = queue.send_message(MessageBody=json.dumps(item))

        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Message pushed {}'.format(response)
            }

def process_new_sport_facility(event, context):
    if event:
        output = json.dumps(event, indent=2, sort_keys=True)
        body = json.loads(event['Records'][0]['body'])
        item = {
                'id' : body['id'],
                'name': body['name'],
                'type': body['type']
            }
        table.put_item(
            Item=item
        )
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Item added: {}'.format(item)
        }
    else:
        return {
            'statusCode': 500,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'No message from queue'
        }

#def update_sport_facility(event,context):
    #TO-DO

def delete_sport_facility(event, context):
    method = event['httpMethod']
    if (method == 'DELETE'):
        id = event['pathParameters']['facility_id']
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
