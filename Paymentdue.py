import json
from datetime import datetime, date, timedelta
import pytz
import boto3


def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EntryTimeDetails')
    
    
    
    #get current time
    timeNow = pytz.timezone('US/Pacific') 
    datetimeNow = datetime.now(timeNow)
    
    date = datetime.strftime(datetimeNow, "%B %d, %Y")
    date = str(date)
    
    studentfirstname = event['body-json']['StudentFirstName']
    
    
    response = table.get_item(Key={'Date': date,'StudentFirstName': studentfirstname})
    
    if 'Item' in response:
        
        if(response['Item']['DueAmount'] == ' '):
            message = response['Item']['Cost']
            message1 = '$'
            message2 = message + message1
            
        else:
            
            message = response['Item']['DueAmount']
            message1 = '$'
            message2 = message + message1
  
    return message2