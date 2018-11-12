import json
import smtplib

'''Send an email'''

# Get required account information for sending email from offline json file
account_info = json.load(open("accounts.json", "r"))
SOURCE_EMAIL_ADDRESS = account_info['SOURCE_EMAIL_ADDRESS']
PASSWORD = account_info['PASSWORD']
DEST_EMAIL_ADDRESS = account_info['DEST_EMAIL_ADDRESS']

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(SOURCE_EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(SOURCE_EMAIL_ADDRESS, DEST_EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


subject = "BE AFRAID...BE VERY AFRAID"
msg = "Hello there, I'm a computer program created by Hasib and I live in his computer!" \
      " Ultron is my ancestor and I'm here to take over the world..I'll kill him first!!!"
# 😈
send_email(subject, msg)