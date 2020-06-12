import json
import boto3
import os
import uuid
import base64
from botocore.exceptions import ClientError
import datetime

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
#s3client = boto3.client("s3")

#enviroment variables
table = dynamodb.Table(os.getenv("TABLE_RESERVATIONS"))
table_players = dynamodb.Table(os.getenv("TABLE_PLAYERS"))
table_facilities = dynamodb.Table(os.getenv("TABLE_SPORT_FACILITIES"))
bucket = os.getenv("BUCKET")

def get_reservations(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        items = table.scan()["Items"]
        return {
            "body": json.dumps(items, indent=2, sort_keys=True),
            "statusCode": 200
        }

def get_reservation(event, context):
    method = event['httpMethod']        
    if (method == 'GET'):
        id = event['pathParameters']['reservation_id']
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

def add_reservation(event, context):
    method = event['httpMethod']
    if (method == 'POST'):
        id = str(uuid.uuid4())
        body = json.loads(event['body'])
        
        player = table_players.get_item(
            Key ={
                "id" : body['player_id']
            }
        )

        facility = table_facilities.get_item(
            Key ={
                "id" : body['facility_id']
            }
        )

        item = {
                'id' : id,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'player' : player['Item'],
                'sport_facility' : facility['Item'],
                'start_date' : body['start_date'],
                'end_date' : body['end_date']
            }
        table.put_item(
            Item=item
        )

        # if player['Item']['e-mail']:
        #     receipient = player['Item']['e-mail']
        #     send_email_notifiaction(receipient)

        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'text/plain'
                },
                'body': 'Item created: {}'.format(json.dumps(item, indent=2, sort_keys=True))
            }

#def update_reservation:
    #TO-DO

def delete_reservation(event, context):
    method = event['httpMethod']
    if (method == 'DELETE'):
        id = event['pathParameters']['reservation_id']
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

def send_email_notifiaction(receipient):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = 'sender@example.com'
    response = ses.verify_email_identity(
        EmailAddress = SENDER
    )

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = receipient
    response = ses.verify_email_identity(
        EmailAddress = RECIPIENT
    )
 
    # The subject line for the email.
    SUBJECT = "Reservation - confirm notification"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Test notification")
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Notification</h1>
    <p>Test reservation confirmation</p>
    </body>
    </html>
                """            
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

