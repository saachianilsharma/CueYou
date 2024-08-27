import random
import smtplib
from email.mime.text import MIMEText
from database import add_otp, get_user_by_email

def send_otp(email):
    user = get_user_by_email(email)
    if not user:
        return False, "Invalid email id"
    
    otp = str(random.randint(100000, 999999))
    add_otp(str(user['_id']), otp)
    
    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = 'OTP for Password Reset'
    msg['From'] = 'youremail@example.com'
    msg['To'] = email
    
    try:
        with smtplib.SMTP('smtp.example.com') as server:
            server.login('youremail@example.com', 'yourpassword')
            server.sendmail('youremail@example.com', [email], msg.as_string())
        return True, "OTP sent successfully"
    except Exception as e:
        return False, str(e)
    