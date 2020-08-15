import json
import boto3
import base64
import uuid

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ParentDetails')
    print(event)
    
    Identificationnumber = event["body-json"]["IdentificationNumber"]
    
    
    resp1 = table.get_item(Key ={"IdentificationNumber" : Identificationnumber})
    
    print(resp1)
    
    if 'Item' not in resp1:
        message = 'IdentificationNumber is not valid'
        
    else:
        
        msg = 'Item found'
        print(msg)
         
          #Decodes the base64 format of the image file
        get_file_content = event["body-json"]["Image"]
        decodecontent = base64.b64decode(get_file_content)
        key = str(Identificationnumber) +'.jpg'
        print(key)
        s3 = boto3.client("s3", region_name = "us-east-2")
        s3upload = s3.put_object(Bucket="east1bucket1", Key = key, Body = decodecontent)
          
          
        lastname = str(resp1['Item']['ParentLastName'])
        
        client=boto3.client('rekognition') 
        
        
          
        response = client.compare_faces(SourceImage={'S3Object': {'Bucket': "east1bucket1", 'Name': key}}, TargetImage={'S3Object': {'Bucket': 'parentspics','Name': key}},)
        
        
        if(len(response['FaceMatches']) == 0):
             message = 'Face not recognized!!!'
            
        else:
              
              
                  # do the database table update change here 
                  
            if ((event["body-json"]["Address"]) == ''):
                 Address = str(resp1['Item']['Address'])
            else:
                 Address = event["body-json"]["Address"] 
                 
                 
            if ((event["body-json"]["Phoneno"]) == ''):
                 Phoneno = str(resp1['Item']['Phoneno'])
            else:
                 Phoneno = event["body-json"]["Phoneno"] 
                  
                  
            if ((event["body-json"]["EmailID"]) == ''):
                 EmailID = str(resp1['Item']['EmailID'])
            else:
                 EmailID = event["body-json"]["EmailID"] 
            
            
            response = table.update_item(Key={'IdentificationNumber': Identificationnumber}, UpdateExpression='SET Address = :val1, Phoneno = :val2, EmailID = :val3',ExpressionAttributeValues={ ':val1': Address, ':val2': Phoneno, ':val3': EmailID})
            message = ''
              

        
       

      
      
    return message
