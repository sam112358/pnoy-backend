from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import config
from flask_cors import CORS
import logging
from fpdf import FPDF
from io import BytesIO
from werkzeug.datastructures import FileStorage
import ssl


app = Flask(__name__)
CORS(app)
app.config.from_object('config')

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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
    message['To'] = EMAIL_RECEIVER
    message['Subject'] = subject

    body = body
    message.attach(MIMEText(body, 'plain'))

    for attachment in attachment_list:
        filename = attachment.name + '.' + attachment.filename.split('.')[1]

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
    logging.info("Mail sent successfully")
    print("Mail Sent Successfully")


@app.route('/api/bookDemo', methods=['POST'])
def submit_enquiry():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    enquiry = data.get('enquiry')

    # Setup PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Email body lines for PDF
    email_body_lines = [
        ("Name", name),
        ("Email", email),
        ("Number", number),
        ("Enquiry", enquiry)
    ]

    for field_name, value in email_body_lines:
        pdf.set_font("Arial", 'B', 12)  # Bold font for field name
        pdf.cell(0, 10, f"{field_name}:", 0, 1)
        pdf.set_font("Arial", size=12)  # Regular font for value
        pdf.cell(0, 10, value, 0, 1)

    # Generate and save PDF
    pdf_filename = f"Enquiry_{name}.pdf"
    pdf.output(pdf_filename)

    # Attach PDF to email
    with open(pdf_filename, "rb") as file:
        pdf_file = FileStorage(stream=file, filename=pdf_filename)
        pdf_file.name = "enquiryDetails"

        # Attach the PDF file
        attachment_list = [pdf_file]

        # Send the email
        send_email(subject="Book Demo", body="Please find the attached enquiry details.", attachment_list=attachment_list)

    # Delete the PDF file after sending the email
    os.remove(pdf_filename)

    return "Email Sent", 200

@app.route('/api/becomeOurDistributor', methods=['POST'])
def submit_details():
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
    pin_code = formData.get('pinCode')

    files = request.files
    gst_details = files.get('gstDetails')
    pan_details = files.get('panDetails')
    aadhaar_details = files.get('aadhaarDetails')
    passport_photo = files.get('passportPhoto')

    email_body_lines = [
        ("Name", name),
        ("Email", email),
        ("Number", number),
        ("Organization Name", organization_name),
        ("Current Business", current_business),
        ("RO Servicing Business", ro_servicing_business),
        ("Client Database", client_database),
        ("Service Executive", service_executive),
        ("Service Calls", service_calls),
        ("Business Address", business_address),
        ("State", state),
        ("City", city),
        ("Pin Code", pin_code)
    ]

    # Generate and save PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for field_name, value in email_body_lines:
        # Set font to bold for field name
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{field_name.upper()}:", 0, 1)
        
        # Set font to regular for field value
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, value, 0, 1)

    pdf_filename = f"Distributor_Details_{name}.pdf"
    pdf.output(pdf_filename)

    with open(pdf_filename, "rb") as file:
        pdf_file = FileStorage(stream=file, filename=pdf_filename)
        pdf_file.name = "distributorDetails"

        # Update the attachment_list
        attachment_list = [gst_details, aadhaar_details, pan_details, passport_photo, pdf_file]

        # Send the email
        send_email(subject=f"Become our distributor : {organization_name}", body=f"PFA the details of the distributor {organization_name}'s application : ", attachment_list=attachment_list)

    # Delete the PDF file after sending the email
    os.remove(pdf_filename)

    return "Email Sent", 200

@app.route('/api/contactUs', methods=['POST'])
def submit_request():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    service_needed = data.get('serviceNeeded')
    state = data.get('state')
    city = data.get('city')

    # Generate and save PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Email body lines for PDF
    email_body_lines = [
        ("Name", name),
        ("Email", email),
        ("Phone Number", number),
        ("Service Needed", service_needed),
        ("Location", f"{city}, {state}")
    ]

    for field_name, value in email_body_lines:
        pdf.set_font("Arial", 'B', 12)  # Bold font for field name
        pdf.cell(0, 10, f"{field_name}:", 0, 1)
        pdf.set_font("Arial", size=12)  # Regular font for value
        pdf.cell(0, 10, value, 0, 1)

    # Generate and save PDF
    pdf_filename = f"Service_Request_{name}.pdf"
    pdf.output(pdf_filename)
    
    # Attach PDF to email
    with open(pdf_filename, "rb") as file:
        pdf_file = FileStorage(stream=file, filename=pdf_filename)
        pdf_file.name = "serviceRequest"

        # Attach the PDF file
        attachment_list = [pdf_file]

        # Send the email
        send_email(subject="Contact Us", body="Please find the attached service request details.", attachment_list=attachment_list)

    # Delete the PDF file after sending the email
    os.remove(pdf_filename)

    return "Email Sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('/etc/letsencrypt/live/pnoy.in/fullchain.pem', '/etc/letsencrypt/live/pnoy.in/privkey.pem'))


# if __name__ == '__main__':
#     if os.getenv('FLASK_SSL', False):
#         # Set SSL context if FLASK_SSL environment variable is set
#         context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#         context.load_cert_chain('/etc/letsencrypt/live/pnoy.in/fullchain.pem', '/etc/letsencrypt/live/pnoy.in/privkey.pem')
#         app.run(host='0.0.0.0', port=443, ssl_context=context, debug=True)
#     else:
#         app.run(host='0.0.0.0', port=5000, debug=True)