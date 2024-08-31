import random
import smtplib
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import sys
from database import add_otp, get_user_by_email


if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
jsonpath = os.path.join(base_path, 'oauth2json', 'clientsecret.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_otp(to):
    user = get_user_by_email(to.strip())
    if not user:
        print ("Invalid email id")
        return False
    otp = str(random.randint(100000, 999999))
    add_otp(str(user['userid']), otp)
    print("otp = ", otp)
    subject = "CueYou - OTP For Password Reset"
    body = "Your OTP for password reset is - "+otp
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(jsonpath, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body)
    message['to'] = to
    message['from'] = 'saachilimns@gmail.com'
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        print(f'Message Id: {message["id"]}')
        return True, "Email sent successfully"
    except Exception as e:
        print(f'An error occurred: {e}')
        return False, str(e)


""" def send_otp(email):
    user = get_user_by_email(email)
    if not user:
        return False, "Invalid email id"
    
    otp = str(random.randint(100000, 999999))
    add_otp(str(user['_id']), otp)
    
    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = 'OTP for Password Reset'
    msg['From'] = 'saachilimns@example.com'
    msg['To'] = email
    
    try:
        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()  # Secure the connection
            server.login('saachilimns@gmail.com', 'limnlimnedsaachi')
            server.sendmail('saachilimns@gmail.com', [email], msg.as_string())
        return True, "OTP sent successfully"
    except Exception as e:
        return False, str(e)
     """

""" def send_email(service):
    try:
        message = MIMEMultipart()
        message['to'] = 'recipient@example.com'
        message['from'] = 'your-email@gmail.com'
        message['subject'] = 'Test Subject'

        body = 'This is a test email body.'
        message.attach(MIMEText(body, 'plain'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Message Id: {message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}') """