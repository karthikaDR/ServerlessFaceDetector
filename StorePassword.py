import json
import boto3
import hashlib
import uuid
import os
import binascii

def lambda_handler(event, context):
    
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ParentDetails')

    
    Identificationnumber = event["body-json"]["IdentificationNumber"]
    
    resp = table.get_item(Key ={"IdentificationNumber" : Identificationnumber})
    
    if 'Item' in resp:
        

        #put your table name here
        __TableName__ = "UserIDtable"
        #put your Primary_key here
        Primary_key = 'IdentificationNumber'
        client = boto3.client('dynamodb')
        DB = boto3.resource('dynamodb')
        table = DB.Table(__TableName__)
        
        EmailID = event['body-json']['EmailId']
        
        #change id2 to your own id
        new_id = Identificationnumber
        #change password2 to your own password 
        new_pass= event["body-json"]["Password"]
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', new_pass.encode('utf-8'),salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        pwd =  (salt + pwdhash).decode('ascii')

        print(pwd)
        sessionvariable = ' '
        table.put_item(Item={'EmailID': EmailID, 'IdentificationNumber': new_id ,'Password': pwd, 'SessionToken' : sessionvariable})
        message = 'Profile saved. Thank you!'
       
    else:
        message = 'IdentificationNumber is not valid'
    
    return message 

    
    

