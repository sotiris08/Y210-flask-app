import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template

def send_welcome_email(email, name):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your account has been created!"
    message["From"] = os.environ['EMAIL_FROM_HEADER']
    message["To"] = email

    text = f"""
    Hi {name}!
    Thank you for creating an account. This email is just to let you know that the process was successful.
    """

    html = render_template('email_welcome.html', name=name);

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    send(email, message)

def send_resetPassword_email(email, name, link):
    message = MIMEMultipart("alternative")
    message["Subject"] = "You have asked to reset your password."
    message["From"] = os.environ['EMAIL_FROM_HEADER']
    message["To"] = email

    text = f"""
        Hi {name},
        
        There was a request to change your password!
        
        If you did not make this request then please ignore this email.
        
        Otherwise, please click this link to change your password: {link}
        """
    html = render_template('email_forgotPassword.html', name=name, link=link)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    send(email, message)

def sendVerificationEmail(email, name, link):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email."
    message["From"] = os.environ['EMAIL_FROM_HEADER']
    message["To"] = email

    text = f"""
            Hi {name},

            You need to verify your email!

            All you have to do is to click on the link below:
            {link}
            """
    html = render_template('email_verificationEmail.html', name=name, link=link)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    send(email, message)

def sendChangedEmailAdressEmail(email, old_email, name):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your email address has been changed"
    message["From"] = os.environ['EMAIL_FROM_HEADER']
    message["To"] = email

    text = f"""
                Hi {name},

                Your email address has been changed from {old_email} to {email}
                This email is just to let you know that the process was successful
                """
    html = render_template('email_changedEmailAdress.html', name=name, old_email=old_email, email=email)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    send(email, message)

def sendMFAViaEmail(email, name, code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your MFA code"
    message["From"] = os.environ['EMAIL_FROM_HEADER']
    message["To"] = email

    text = f"""
            Hi {name},

            Here is your MFA code: {code}
            This code is valid for 5 minutes
        
            If you did not make this request then please ignore this email.
            """
    html = render_template('email_mfaViaEmail.html', name=name, code=code)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    send(email, message)

def send(email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ['EMAIL_SMTP_SERVER_IP'], os.environ['EMAIL_SMTP_SERVER_PORT'],context=context) as server:
        server.login(os.environ['EMAIL_SMTP_SERVER_LOGIN'], os.environ['EMAIL_SMTP_SERVER_PASSWORD'])
        server.sendmail(os.environ['EMAIL_FROM_HEADER'], email, message.as_string())