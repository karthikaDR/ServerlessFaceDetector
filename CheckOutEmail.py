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

			if record['eventName'] == 'MODIFY':

				handle_modify(record)
				
		
		print('------------------------')

		return "Success!"

	except Exception as e: 

		print(e)

		print('------------------------')

		return "Error"


def handle_modify(record):

	print("Handling ModIFY Event")
	
	#3a.Parse oldImage and check_out
	oldImage = record['dynamodb']['OldImage']
	FirstName = oldImage['StudentFirstName']['S']
	Check_in = oldImage['Checkin']['S']
	DateDay = oldImage['Date']['S']
	emailAddress = oldImage['EmailID']['S']
	
	#3b. Parse newImage and check_out.
	newImage = record['dynamodb']['NewImage']
	Check_out = newImage['Checkout']['S']
	Sendemail = newImage['SendEmail']['S']
	
	
	
	print('Done handling MODIFY event')
	
	
	
	SENDER ="karthikagodwin@gmail.com"
	RECIPIENT= emailAddress
	SENDERNAME = 'Kids n Play'
	
	# Replace smtp_username with your Amazon SES SMTP user name.
	USERNAME_SMTP = ""
	# Replace smtp_password with your Amazon SES SMTP password.
	PASSWORD_SMTP = ""
	
	HOST = "region"
	PORT = 587
	
	# The subject line of the email.
	SUBJECT = 'Entry time details'
	
	# The HTML body of the email.
	BODY_HTML = """<html>
	<head></head>
	<body>
	<p> Dear Parent, </p>
	<p> Please find the check-in/check-out time details of your child below. </p>
	<p> Date:
	""" + str(FirstName) + """</p>
	<p> Date:
	""" + str(DateDay) + """</p>
	<p> Check-in:
	""" + str(Check_in) + """</p>
	<p> Check-out:
	""" + str(Check_out) + """</p>
	<br>
	<br>
	<br>
	<p> Thank you, </p>
	<p> Kids n Play </p>
	   
	</body>
	</html>
	    """
	
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
	
	if(Sendemail == 'X'):

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
