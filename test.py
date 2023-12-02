import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email and password
username = 'samarthkhandelwal39temp@gmail.com'
password = 'sncg nyzw ipxh ywtk'  # Replace with your app-specific password

# Create the multipart message and set headers
message = MIMEMultipart()
message['From'] = username
message['To'] = 'samarth.khandelwal39@gmail.com'
message['Subject'] = 'Subject - Sending Document'

# Body of the email
body = "This is the body of the email. The document is attached."
message.attach(MIMEText(body, 'plain'))

# Attach a document
filename = 'app.py'  # Replace with your file name
attachment = open(filename, 'rb')  # Open the file in binary mode

# Instance of MIMEBase and named as part
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header('Content-Disposition', f"attachment; filename= {filename}")

# Attach the instance 'part' to MIMEMultipart message
message.attach(part)

# Start the SMTP server and send the email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(username, password)

# Convert the message to a string and send it
server.send_message(message)

# Close the server
server.quit()
print("Mail Sent Successfully")
