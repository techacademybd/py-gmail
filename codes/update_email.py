import gspread
from oauth2client.service_account import ServiceAccountCredentials
import imaplib
import email
import json
from collections import defaultdict
import pandas as pd

'''Read the latest email and updates the message content in google sheets
'''

# get credentials
ACCOUNT_INFO = json.load(open("accounts.json", "r"))
FROM_EMAIL = ACCOUNT_INFO['SOURCE_EMAIL_ADDRESS']
FROM_PWD = ACCOUNT_INFO['PASSWORD']

# login with credentials and get inbox data
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(FROM_EMAIL, FROM_PWD)
mail.list()
mail.select("inbox")

# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com
credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)
# open ss
worksheet = gc.open('test')
wks_1 = worksheet.get_worksheet(5)
# wks_1 = worksheet.worksheet("Sheet 6")


# convert raw message block to READABLE text
def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

# read emails from inbox
def get_email(counter): # counter: read how many emails?

    result, data = mail.search(None, "ALL")
    # data is a list
    ids = data[0]
    # ids is a space separated string
    id_list = ids.split()
    # get the latest email in the inbox stack
    
    counter = -counter
    latest_email_id = id_list[counter]

    # get raw email
    _, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]

    decoded_raw_email = raw_email.decode()
    email_message = email.message_from_string(decoded_raw_email)
    # convert raw email to text
    message = get_first_text_block(email_message)
    # print(str(email.utils.parseaddr(email_message['From'])[0]))
    name = str(email.utils.parseaddr(email_message['From'])[0])

    # twats sending long texts!
    if len(message) > 100:
        message = message[:100]
    return name, message

# counter to check emails
count = 8
# store name of sender and message in dictionary
book = defaultdict(list) 


# store person: message in google sheets
for i in range(count):
    i+=1
    name, msg = get_email(i)
    book[name].append(msg)
    wks_1.update_cell(i+1, 1, name)
    wks_1.update_cell(i+1, 2, msg)


# dataframe to store the book locally
dt = pd.DataFrame(columns=['Person', "Message"])
dt['Person'] = book.keys()
dt['Message'] = book.values()

# save  the file if records need to be kept locally
#dt.to_csv('book.csv')
#dt = pd.read_csv('book.csv')

# debug for visualizations
'''
Email: str(email.utils.parseaddr(email_message['From'])[1]))
Name: str(email.utils.parseaddr(email_message['From'])[0]))
Email subject: str(email_message['Subject']))
Message: str(message))
'''

'''Put logic here:
    If name is in column then update message block in THAT column
'''
# read the nth email from top
# _, message = get_email(9)
# print(message)


print("Done!")

# go here before running script to see demo
# https://docs.google.com/spreadsheets/d/140vlBiZmISWAueX-rAOQMX0QL3e7ygyIbYkPA4ORTTk/edit?usp=sharing

