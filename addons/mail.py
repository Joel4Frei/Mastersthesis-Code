import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Set up the sender and recipient email addresses
def send_mail_exp(variable,subject):
    sender_email = "microscope.py@outlook.com"
    recipient_email = "microscope.py@gmail.com"

    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = "tksispyfndupbdqg"  # Generate this in your Outlook/Hotmail account settings

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    current_time = time.localtime()
    current_time = time.strftime('%H:%M:%S',current_time)

    if variable == 0:
        msg = 'Starting the experiment.'
        body = f"{msg}\n{current_time}"
    else:
        msg = f'Starting Cycle Nr. {variable}.'
        body = f"The experiment is running succsefully.\n{msg}\n {current_time}"


    
    message.attach(MIMEText(body, "plain"))

    # Connect to the Outlook/Hotmail SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use STARTTLS for security
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print('Email sent!')



def send_mail(text,subject):
    sender_email = "microscope.py@outlook.com"
    recipient_email = "microscope.py@gmail.com"

    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = "tksispyfndupbdqg"  # Generate this in your Outlook/Hotmail account settings

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    current_time = time.localtime()
    current_time = time.strftime('%H:%M:%S',current_time)

    body = text

    message.attach(MIMEText(body, "plain"))

    # Connect to the Outlook/Hotmail SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use STARTTLS for security
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print('Email sent!')
