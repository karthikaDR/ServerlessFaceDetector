import json
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print('Loading function')

def lambda_handler(event, context):

	print('------------------------')

	print(event)

	#1. Iterate over each record

	try:

		for record in event['Records']:

			#2. Handle event by type

			if record['eventName'] == 'INSERT':

				handle_insert(record)
				

		print('------------------------')

		return "Success!"

	except Exception as e: 

		print(e)

		print('------------------------')

		return "Error"

def handle_insert(record):

	print("Handling INSERT Event")

	#3a. Get newImage content

	newImage = record['dynamodb']['NewImage']

	#3b. Parse values

	newaddress = newImage['EmailID']['S']
	new_id = newImage['IdentificationNumber']['S']
	
	#3c. Print it
	
	

	SENDER ="karthikagodwin@gmail.com"
	RECIPIENT= newaddress
	SENDERNAME = 'Kids n Play'
	
	# Replace smtp_username with your Amazon SES SMTP user name.
	USERNAME_SMTP = ""
	# Replace smtp_password with your Amazon SES SMTP password.
	PASSWORD_SMTP = ""

	# (Optional) the name of a configuration set to use for this message.
	# If you comment out this line, you also need to remove or comment out
	# the "X-SES-CONFIGURATION-SET:" header below.
#	CONFIGURATION_SET = "ConfigSet"

	# If you're using Amazon SES in an AWS Region other than US West (Oregon), 
	# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
	# endpoint in the appropriate region.
	HOST = "region"
	PORT = 587

	# The subject line of the email.
	SUBJECT = 'Important: Registration number'


	# The HTML body of the email.
	BODY_HTML = """<html>
	<head></head>
	<body>
	  <h4>Dear Parent,</h4>
	  <p> Thank you for registering with us</p>
	  <p>Given is your registration/identification number:<b>
	  """ + str(new_id) + """</b></p>
      <p>Please <a href= "https://parentfacenprofile.s3.us-east-2.amazonaws.com/Passwordactivation.html" target = "_blank"> click here </a>
      to create password and activate your account.</p><br><br><br>
      <p>Thank you,</p>
      <p>Kids n Play</p>
	</body>
	</html>"""
           

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = SUBJECT
	msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
	msg['To'] = RECIPIENT
	
	# Comment or delete the next line if you are not using a configuration set
	#msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(BODY_TEXT, 'plain')
	part2 = MIMEText(BODY_HTML, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	#msg.attach(part1)
	msg.attach(part2)

	# Try to send the message.
	try:
		server = smtplib.SMTP(HOST, PORT)
		server.ehlo()
		server.starttls()
		#stmplib docs recommend calling ehlo() before & after starttls()
		server.ehlo()
		server.login(USERNAME_SMTP, PASSWORD_SMTP)
		server.sendmail(SENDER, RECIPIENT, msg.as_string())
		server.close()
		# Display an error message if something goes wrong.
	except Exception as e:
		print ("Error: ", e)
	else:
		print ("Email sent!")
