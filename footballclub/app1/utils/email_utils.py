# utils/email_utils.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'edwinraju2024a@mca.ajce.in'
EMAIL_HOST_PASSWORD = '90483445567'

def send_email(subject, body, to_email, password, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    # Include the password in the email body
    body_with_password = f"{body}\n\nYour password is: {password}"
    msg.attach(MIMEText(body_with_password, 'html'))

    if attachment:
        try:
            with open(attachment, "rb") as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
            msg.attach(part)
        except OSError as e:
            print(f"Error attaching file: {str(e)}")

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
