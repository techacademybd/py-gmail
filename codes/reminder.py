import json
import smtplib
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Credentials file for Google Sheets
cred_file = 'Sheets Test2-316f8201c13e.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# Get required account information for sending email from offline json file
account_info = json.load(open("accounts.json", "r"))
SOURCE_EMAIL_ADDRESS = account_info['SOURCE_EMAIL_ADDRESS']
PASSWORD = account_info['PASSWORD']
DEST_EMAIL_ADDRESS = account_info['DEST_EMAIL_ADDRESS']

# Email subject and body
subject = "Class Documentation"
message = "What happened in class today?"

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


# authorize
gc = gspread.authorize(credentials)

# open ss
worksheet = gc.open('test')

# sheet 7 ("demo")
wks_1 = worksheet.worksheet('demo')


# Get today's date and day of week
date_time = datetime.datetime.now()
today = date_time.strftime("%A")
checker = date_time.strftime("%d/%m/%Y")

# Get the column number for today
COLUMN = wks_1.find(today).col

# Get all dates of this weekday from the sheet
dates = wks_1.col_values(COLUMN)[4:]
dates = [x for x in dates if x]

# Send reminder if no data in today's documentation

# Try to find today's date on sheet
if checker in dates:
    found = wks_1.find(checker)
    r, c = found.row, found.col
    # If date found but not documented, send email
    if wks_1.cell(r,c+2).value == "":
        send_email(subject, message)
    else:
        print(":)")

# If today's date is not found, insert date and student names
else:
    last = wks_1.find(dates[-1])
    r, c = last.row, last.col
    # Insert current date
    wks_1.update_cell(r+9, c, checker)

    # Insert student names
    # Special case for Saturday
    if(today == "Saturday"):
        for i in range(4):
            row = r
            column = c + 1 + i*2
            students = wks_1.col_values(column)[row-1:r+8]
            for student in students:
                wks_1.update_cell(row+9, column, student)
                row = row + 1
    # For all other days
    else:
        students = wks_1.col_values(c + 1)[r-1:r+8]
        for student in students:
                wks_1.update_cell(r+9, c + 1, student)
                r = r + 1

    # Send email
    send_email(subject, message)
