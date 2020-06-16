import json
import boto3
import os
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
client_lambda = boto3.client('lambda')
s3client = boto3.client("s3")

#enviroment variables
table = dynamodb.Table(os.getenv("TABLE_EVENTS"))
table_players = dynamodb.Table(os.getenv("TABLE_PLAYERS"))
table_reservations = dynamodb.Table(os.getenv("TABLE_RESERVATIONS"))
table_facilities = dynamodb.Table(os.getenv("TABLE_SPORT_FACILITIES"))
bucket = os.getenv("BUCKET")


def get_events(event, context):
    method = event['httpMethod']
    if (method == 'GET'):
        items = table.scan()["Items"]
        return {
            "body": json.dumps(items, indent=2, sort_keys=True),
            "statusCode": 200
        }


def get_event(event, context):
    method = event['httpMethod']
    if (method == 'GET'):
        id = event['pathParameters']['event_id']
        item = table.get_item(
            Key={"id": id}
        )
        item = item['Item']
        return {
            "body": json.dumps(item, indent=2, sort_keys=True),
            "statusCode": 200
        }


def add_event(event, context):
    id = str(uuid.uuid4())
    body = json.loads(event['body'])

    reservation_body = {
        "player_id": body['player_id'],
        "facility_id": body['facility_id'],
        "start_date": body['start_date'],
        "end_date": body['end_date']
    }

    reservation = client_lambda.invoke(
        FunctionName=os.getenv("LAMBDA_ADD_RESERVATION_ARN"),
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(reservation_body),
    )
   
    reservation_body = json.load(reservation['Payload'])
    if 'body' in reservation_body:
        reservation_body = json.loads(reservation_body['body'])

    item = {
        'id': id,
        'name': body['name'],
        'reservation': reservation_body,
        "teams": body['teams'],
        "players": 'players_list'
    }

    table.put_item(Item=item)
    return {
        'statusCode':
        200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body':
        'Item created: {}'.format(json.dumps(item, indent=2, sort_keys=True))
    }


def delete_event(event, context):
    method = event['httpMethod']
    if (method == 'DELETE'):
        id = event['pathParameters']['event_id']
        table.delete_item(Key={"id": id})
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Item deleted: {}'.format(str(id))
        }
