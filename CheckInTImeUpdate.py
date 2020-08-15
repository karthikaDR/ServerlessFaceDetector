import json
from datetime import datetime, date, timedelta
import pytz
import boto3



def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ParentDetails')
    print(event)

    #get the student details and store the time in 'TimeDetails' table
    Identificationnumber = event["body-json"]["IdentificationNumber"]
    sendemail = event['body-json']['SendEmail']
    resp = table.get_item(Key = {"IdentificationNumber" : Identificationnumber})
    

    print(resp)
    
    if 'Item' in resp:
        #get student details
        studentlastname = str(resp['Item']['StudentLastName'])
        studentfirstname = str(resp['Item']['StudentFirstName'])
        emailID = str(resp['Item']['EmailID'])
        classroomnumber = str(resp['Item']['ClassroomNumber'])
        
        
        
        #get current time
        timeNow = pytz.timezone('US/Pacific') 
        datetimeNow = datetime.now(timeNow)
        date_time = str(datetime.strftime(datetimeNow, "%B %d, %Y %H:%M"))

        
        

        table = dynamodb.Table('EntryTimeDetails')
        
        
        if((event["body-json"]["Entry"]) == 'Checkin'):
            date = datetime.strftime(datetimeNow, "%B %d, %Y")
            date = str(date)
            time = datetime.strftime(datetimeNow, "%I:%M:%S %p")
            time = str(time)
            checkouttime = ' '
            hours = ' '
            cost = ' '
            amountpaid = ' '
            amountdue = ' '
            response = table.put_item(Item={'EmailID': emailID, 'StudentFirstName': studentfirstname, 'StudentLastName': studentlastname,
                                             'ClassroomNumber': classroomnumber, 'Checkin' : time, 'Checkout' : checkouttime, 
                                             'Hours' : hours, 'Cost': cost, 'AmountPaid': amountpaid, 'DueAmount': amountdue, 
                                             'SendEmail': sendemail, 'Datetime' : date_time, 'Date': date})
        else:
          
            #Checkout time details
            date = datetime.strftime(datetimeNow, "%B %d, %Y")
            date = str(date)
            resp1 = table.get_item(Key ={"Date" : date, "StudentFirstName" : studentfirstname})
            checkintime = str(resp1['Item']['Datetime'])
            
            #Check in time details
            checkin_time = datetime.strptime(checkintime, '%B %d, %Y %H:%M')
            print(checkin_time)
             
            
            

            time = datetime.strftime(datetimeNow, "%I:%M:%S %p")
            print(time)
            checkout_time = datetime.strptime(date_time, '%B %d, %Y %H:%M')
            print(checkout_time)
            time = str(time)
            checkouttime = time
            
            difference = checkout_time - checkin_time
            timedifference = (difference.total_seconds())/60
            print(timedifference)
            totalcost = (timedifference * 8)/100
            totalcost = str(totalcost)
            timedifference = timedifference/24
            timedifference = str(timedifference)
            
            
            
            response = table.update_item(Key={'Date': date, 'StudentFirstName': studentfirstname}, UpdateExpression='SET Checkout = :val1, Hours = :val2, Cost = :val3',ExpressionAttributeValues={ ':val1': checkouttime, ':val2': timedifference, ':val3' : totalcost})
                                             
            
        