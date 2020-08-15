import json
import pytz
import boto3
import base64
import uuid
from datetime import datetime
    


def lambda_handler(event, context):
    
        
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ParentDetails')

    
    Identificationnumber = event["body-json"]["IdentificationNumber"]
    
    
    resp = table.get_item(Key ={"IdentificationNumber" : Identificationnumber})
    
    
    if 'Item' in resp:
      msg = 'Item found'
      
      client = boto3.client('lambda')
      #Call the update time function to upload the checkin/checkout time of the student           
      response1 = client.invoke(FunctionName='Updatetime',
                                InvocationType='Event',
                                Payload=json.dumps(event))
     
      #Decodes the base64 format of the image file
      get_file_content = event["body-json"]["Image"]
      decodecontent = base64.b64decode(get_file_content)
      key = str(Identificationnumber) +'.jpg'
      print(key)
      s3 = boto3.client("s3", region_name = "us-east-2")
      s3upload = s3.put_object(Bucket="east1bucket1", Key = key, Body = decodecontent)
      
      
      lastname = str(resp['Item']['ParentLastName'])

    
      client=boto3.client('rekognition') 
    

      
      response = client.compare_faces(SourceImage={'S3Object': {'Bucket': "east1bucket1", 'Name': key}}, TargetImage={'S3Object': {'Bucket': 'parentspics','Name': key}},)
    
      print(len(response['FaceMatches']))
      if(len(response['FaceMatches']) == 0):
         message = 'Face not recognized. Access denied!!!'
            
      else:
         message1 = ', Your Access granted!!!' 
         message2 = 'Hello '
         message = message2 + lastname + message1 
         



        
    
    else:
      message = 'IdentificationNumber is not valid'

    
    return message


    # # TODO implement
    # return {
    #     'statusCode': 200,
    #     'headers': {"Access-Control-Allow-Origin": "*",
    #                 "Access-Control-Allow-Headers":"Content-Type",
    #                 "Access-Control-Allow-Methods": "POST,GET,OPTIONS"},

    #     'body': json.dumps(message)
    # }
