import json
import boto3
import os
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
s3client = boto3.client("s3")
rekog = boto3.client('rekognition')

#enviroment variables
table = dynamodb.Table(os.getenv("TABLE_PLAYERS"))
bucket = os.getenv("BUCKET")

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
        id = str(uuid.uuid4())
        body = json.loads(event['body'])
        photo = upload_photo(id,body,body['photo'])
        item = {
                'id' : id,
                'login': body['login'],
                'first_name': body['first_name'],
                'last_name': body['last_name'],
                'birth_date': body['birth_date'],
                'team': body['team'],
                'photo': photo
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

def upload_photo(id, body, photo):
    uid = str(id) + ".jpg"

    response = rekog.detect_faces(
        Image={
            'Bytes': base64.b64decode(photo)
        }
    )
    confidence = 0
    
    if (len(response['FaceDetails']) == 1):
        confidence = response['FaceDetails'][0]['Confidence']
        
    if confidence > 80.:
        s3client.put_object(
            Bucket=bucket,
            Key=uid,
            Body=base64.b64decode(photo),
            ACL="public-read",
        )
        return get_public_url(bucket,uid)
    else:
        return 'Bad photo'

def get_public_url(bucket, key):
    return "https://s3.us-east-1.amazonaws.com/{}/{}".format(bucket, key)