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
    amountpaid = event['body-json']['AmountPaid']
    
    response = table.get_item(Key={'Date': date,'StudentFirstName': studentfirstname})
    
    if 'Item' in response:
     
      if(response['Item']['DueAmount'] == ' '):
          x = float(response['Item']['Cost'])
          y = float(amountpaid)
          
          Dueamount = x - y
      else:
          x = float(response['Item']['DueAmount'])
          y = float(amountpaid)
          
          Dueamount = x - y
        
      dueamount = str(Dueamount)
      
      if(dueamount <= '0.0'):
        dueamount = '0.0'
        message = 'Thank you for your payment. No amount due.'
      else:
        message1 = 'Thank you for your payment. The amount due is '
        message2 = dueamount
        message3 = '$'
        message = message1 + message2 + message3
      
      #Update the amount due
      response = table.update_item(Key={'Date': date, 'StudentFirstName': studentfirstname}, UpdateExpression='SET DueAmount = :val1',ExpressionAttributeValues={':val1': dueamount})
      

      
      
    else:
        
      message = 'No due amount exist for today`s date'
    
    
    return message