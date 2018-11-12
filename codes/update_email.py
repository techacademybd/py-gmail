import gspread
from oauth2client.service_account import ServiceAccountCredentials
import imaplib
import email

'''Read the latest email and updates the message content in google sheets
'''

# sender email and password
FROM_EMAIL = "techacademy1234@gmail.com"
FROM_PWD = "TESTtta1234"


# convert raw message block to READABLE text
def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


# login with credentials and get inbox data
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(FROM_EMAIL, FROM_PWD)
mail.list()
mail.select("inbox")

result, data = mail.search(None, "ALL")

# data is a list
ids = data[0]

# ids is a space separated string
id_list = ids.split()

# get the latest email in the inbox stack
latest_email_id = id_list[-1]

# get raw email
_, data = mail.fetch(latest_email_id, "(RFC822)")
raw_email = data[0][1]

# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)

SOURCE_EMAIL_ADDRESS = "techacademy1234@gmail.com"
PASSWORD = "TESTtta1234"

# open ss
worksheet = gc.open('test')

# main order cart
wks_1 = worksheet.get_worksheet(5)
# wks_1 = worksheet.worksheet("Sheet 1")

decoded_raw_email = raw_email.decode()
email_message = email.message_from_string(decoded_raw_email)

# convert raw email to text
message = get_first_text_block(email_message)

print("Sent from: " + str(email.utils.parseaddr(email_message['From'])[1]))
print("\n")
print("Email subject: " + str(email_message['Subject']))
print("\n")
print("Message: " + str(message))

'''Put logic here:
    If name is in column then update message block in that column
'''

for i in range(2):
    wks_1.update_cell(i+2, 2, message)
