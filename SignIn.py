import json
import boto3
import hashlib
import uuid
import os
import binascii


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserIDtable')
    salt = ''
    
    EmailID = event['body-json']['EmailID']
    entered_password = event['body-json']['Password']
    
    
    resp = table.get_item(Key ={"EmailID" : EmailID})
    
    password = event["body-json"]["Password"]
    
    if 'Item' in resp:
       database_password = resp['Item']['Password']
       
       salt = database_password[:64]
       database_password = database_password[64:]
       pwdhash = hashlib.pbkdf2_hmac('sha512',entered_password.encode('utf-8'), salt.encode('ascii'), 100000)
       pwdhash = binascii.hexlify(pwdhash).decode('ascii')


       print(pwdhash)
       print(database_password)
       if (pwdhash != database_password):
           message = 'Password is invalid'
       else:
           message = ''
       if '@csun.edu' in EmailID:
           message = 'admin'
       else:
           message = 'user'
    else:
        message = 'Invalid Login'
    


    #Check id and password match from database 
    # TODO implement
    return message
    
    """{
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers":"Content-Type",
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS"},

        'body': json.dumps(message)
    }"""