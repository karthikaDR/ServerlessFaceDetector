import json
import boto3
import base64
import uuid
import random

def lambda_handler(event, context):
    
    s3 = boto3.client("s3", region_name = "us-east-2")
    
  
    
    #Decodes the base64 format of the image file
    get_file_content = event["body-json"]["Image"]
    decodecontent = base64.b64decode(get_file_content)
    
    #Get the number of counts present in the database table and accordingly allocate the identification number for the parent.
    client = boto3.client('dynamodb')
    response = client.describe_table(TableName='ParentDetails')
    print(response['Table']['ItemCount'])
    
    #Generate random four digit id
    uuid1 = random.randint(10000,99999)

    
    #Upload the image with name as 'uuid.jpg'
    #IdentificationNumber = response['Table']['ItemCount'] + 1
    key = (str(uuid1)) + '.jpg' 
    s3upload = s3.put_object(Bucket="parentspics", Key = key, Body = decodecontent)
    
    #Update database table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('ParentDetails')
    parentfirstname = event["body-json"]["ParentFirstName"]
    parentlastname = event["body-json"]["ParentLastName"]
    relation = event["body-json"]["Relation"]
    emailID = event["body-json"]["EmailID"]
    address = event["body-json"]["Address"]
    phoneno = event["body-json"]["Phoneno"]
    studentfirstname = event["body-json"]["StudentFirstName"]
    studentlastname = event["body-json"]["StudentLastName"]
    studentdob = event["body-json"]["StudentDOB"]
    studentgender = event["body-json"]["StudentGender"]
    classroom = event["body-json"]["ClassroomNumber"]
    
    
    uuid1 = str(uuid1)
   
    response = table.put_item(Item={'ParentFirstName': parentfirstname,'ParentLastName': parentlastname,
                                    'Relation': relation, 'EmailID' : emailID, 'Address' : address,
                                    'Phoneno': phoneno, 'StudentFirstName': studentfirstname, 'StudentLastName': studentlastname,
                                    'StudentDOB': studentdob, 'StudentGender': studentgender, 'IdentificationNumber': uuid1, 
                                    'ClassroomNumber': classroom  })


   
    
    message = 'success'
    
    
    
    # TODO implement
    return message
    

