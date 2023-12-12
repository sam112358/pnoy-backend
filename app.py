from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import config
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object('config')

# Use the configuration
EMAIL_HOST = app.config['EMAIL_HOST']
EMAIL_PORT = app.config['EMAIL_PORT']
EMAIL_HOST_USER = app.config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = app.config['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = app.config['EMAIL_USE_TLS']
EMAIL_RECEIVER = app.config['EMAIL_RECEIVER']

def create_file(content):
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = file.filename
        file.save(os.path.join(filename))
        return f'File {filename} uploaded successfully', 200

def send_email(subject, body, attachment_list):
    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = 'samarth.khandelwal39@gmail.com'
    message['Subject'] = subject

    # Body of the email
    body = body
    message.attach(MIMEText(body, 'plain'))

    for attachment in attachment_list:
        filename = 'app.py'
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())

        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f"attachment; filename= {filename}")

        message.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    server.send_message(message)

    server.quit()
    print("Mail Sent Successfully")


@app.route('/bookDemo', methods=['POST'])
def submit_enquiry():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    enquiry = data.get('enquiry')

    email_body = f'Name : {name}\nEmail : {email}\nNumber : {number}\nEnquiry : {enquiry}'

    send_email(subject="Book Demo", body=email_body, attachment_list=[])
    
    return "Email Sent", 200

@app.route('/becomeOurDistributor', methods=['POST'])
def submit_details():
    # data = request.json
    formData = request.form
    name = formData.get('name')
    email = formData.get('email')
    number = formData.get('number')
    organization_name = formData.get('organizationName')
    current_business = formData.get('currentBusiness')
    ro_servicing_business = formData.get('ROServicingBusiness')
    client_database = formData.get('clientDatabase')
    service_executive = formData.get('serviceExecutive')
    service_calls = formData.get('serviceCalls')
    business_address = formData.get('businessAddress')
    state = formData.get('state')
    city = formData.get('city')

    files = request.files
    gst_details = files.get('gstDetails')
    pan_details = files.get('panDetails')
    aadhaar_details = files.get('aadhaarDetails')

    email_body = f"""
        Name : {name}
        Email : {email}
        Number : {number}
        Organization Name : {organization_name}
        Current Business : {current_business}
        RO Servicing Business : {ro_servicing_business}
        Client Database : {client_database}
        Service Executive : {service_executive}
        Service Calls : {service_calls}
        Business Address : {business_address}
        State : {state}
        City : {city}
        GST Details : {gst_details}
        PAN Details : {pan_details}
        Aadhaar Details : {aadhaar_details}"""
    
    send_email(subject="Book Demo", body=email_body, attachment_list=[gst_details, aadhaar_details, pan_details])

    return "Email Sent", 200

@app.route('/contactUs', methods=['POST'])
def submit_request():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    service_needed = data.get('serviceNeeded')
    state = data.get('state')
    city = data.get('city')

    email_body = f"""
        Name: {name}
        Email: {email}
        Phone Number: {number}
        Service Needed: {service_needed}
        Location: {city}, {state}"""
    
    return "Email Sent", 200

if __name__ == '__main__':
    app.run(debug=True)
