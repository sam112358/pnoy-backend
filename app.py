from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email configuration
# Email configuration for Gmail
EMAIL_HOST = 'smtp.gmail.com' # Gmail SMTP server
EMAIL_PORT = 587 # SMTP port for Gmail (TLS)
EMAIL_HOST_USER = 'samarthkhandelwal39temp@gmail.com' # Your Gmail address
EMAIL_HOST_PASSWORD = 'sncg nyzw ipxh ywtk' # Your Gmail password or App Password
EMAIL_USE_TLS = True
EMAIL_RECEIVER = 'samarth.khandelwal39@gmail.com' # Email where you want to receive messages


def send_email(name, phone, comments):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = 'New Contact Information Received'

    body = f"Name: {name}\nPhone: {phone}\nComments: {comments}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    if EMAIL_USE_TLS:
        server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_HOST_USER, EMAIL_RECEIVER, text)
    server.quit()

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    comments = data.get('comments')

    if not all([name, phone, comments]):
        return jsonify({'error': 'Missing fields'}), 400

    send_email(name, phone, comments)
    return jsonify({'message': 'Email sent successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
