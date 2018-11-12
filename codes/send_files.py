import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''Send an email with attachments
     ref: http://naelshiab.com/tutorial-send-email-python/
'''
# Get required account information for sending email from offline json file
account_info = json.load(open("accounts.json", "r"))
fromaddr = account_info['SOURCE_EMAIL_ADDRESS']
PASSWORD = account_info['PASSWORD']
toaddr = account_info['DEST_EMAIL_ADDRESS']

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Attachment test"

body = "Please find below the TTA logo attached."

msg.attach(MIMEText(body, 'plain'))

filename = "tta.png"
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

'''
# multiple files

filenames = ["a.png", "l.png"]

for f in filenames:
    attachment = open(f, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % f)
    msg.attach(part)

'''


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, PASSWORD)
text = msg.as_string()

server.sendmail(fromaddr, toaddr, text)
server.quit()
print("Sent!")


# read email(works in python2) https://codehandbook.org/how-to-read-email-from-gmail-using-python/
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
# https://pythonprogramminglanguage.com/read-gmail-using-python/
