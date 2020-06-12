import json
import boto3
import os
import uuid
import base64
from botocore.exceptions import ClientError
import datetime

dynamodb = boto3.resource('dynamodb')
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
        print(json.dumps(body, indent=2))
        
        player = table_players.get_item(
            Key ={
                "id" : body['player_id']
            }
        )
        print(player)

        facility = table_facilities.get_item(
            Key ={
                "id" : body['facility_id']
            }
        )
        print(facility)

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

# def send_email_notifiaction():
#     # Replace sender@example.com with your "From" address.
#     # This address must be verified with Amazon SES.
#     SENDER = "Sender Name <sender@example.com>"

#     # Replace recipient@example.com with a "To" address. If your account 
#     # is still in the sandbox, this address must be verified.
#     RECIPIENT = "recipient@example.com"

#     # Specify a configuration set. If you do not want to use a configuration
#     # set, comment the following variable, and the 
#     # ConfigurationSetName=CONFIGURATION_SET argument below.
#     CONFIGURATION_SET = "ConfigSet"

#     # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
#     AWS_REGION = "us-west-2"

#     # The subject line for the email.
#     SUBJECT = "Amazon SES Test (SDK for Python)"

#     # The email body for recipients with non-HTML email clients.
#     BODY_TEXT = ("Amazon SES Test (Python)\r\n"
#                 "This email was sent with Amazon SES using the "
#                 "AWS SDK for Python (Boto)."
#                 )
                
#     # The HTML body of the email.
#     BODY_HTML = """<html>
#     <head></head>
#     <body>
#     <h1>Amazon SES Test (SDK for Python)</h1>
#     <p>This email was sent with
#         <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
#         <a href='https://aws.amazon.com/sdk-for-python/'>
#         AWS SDK for Python (Boto)</a>.</p>
#     </body>
#     </html>
#                 """            

#     # The character encoding for the email.
#     CHARSET = "UTF-8"

#     # Create a new SES resource and specify a region.
#     client = boto3.client('ses',region_name=AWS_REGION)

#     # Try to send the email.
#     try:
#         #Provide the contents of the email.
#         response = client.send_email(
#             Destination={
#                 'ToAddresses': [
#                     RECIPIENT,
#                 ],
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': CHARSET,
#                         'Data': BODY_HTML,
#                     },
#                     'Text': {
#                         'Charset': CHARSET,
#                         'Data': BODY_TEXT,
#                     },
#                 },
#                 'Subject': {
#                     'Charset': CHARSET,
#                     'Data': SUBJECT,
#                 },
#             },
#             Source=SENDER,
#             # If you are not using a configuration set, comment or delete the
#             # following line
#             ConfigurationSetName=CONFIGURATION_SET,
#         )
#     # Display an error if something goes wrong.	
#     except ClientError as e:
#         print(e.response['Error']['Message'])
#     else:
#         print("Email sent! Message ID:"),
#         print(response['MessageId'])

