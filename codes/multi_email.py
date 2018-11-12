import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib

'''Send emails to multiple accounts as selected from the spreadsheets
'''

SOURCE_EMAIL_ADDRESS = "techacademy1234@gmail.com"
PASSWORD = "TESTtta1234"

# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)

# open ss
worksheet = gc.open('test')

# target email list
wks_1 = worksheet.get_worksheet(5)

# list of people with their email addresses
wks_2 = worksheet.get_worksheet(6)


def empty_string(val):
    if len(val) == 0:
        raise ValueError("String is empty, SYSTEM ANGRY!")
    else:
        return val


def comp_list(comps):
    if len(comps) == 0:
        raise ValueError("You don't have anything on the order cart! What do you expect me to order?")
    else:
        return comps


def send_email(subject, dest, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(SOURCE_EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(SOURCE_EMAIL_ADDRESS, dest, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


subject = "BE AFRAID...BE VERY AFRAID"
msg = "Hello there, I'm a computer program created by Hasib and I live in his computer!" \
      " Ultron is my ancestor and I'm here to take over the world..I'll kill him first!!!"

# go to sheet 1 and get the value of the target email persons
values_list = comp_list(wks_1.col_values(1)[1:])
# print(values_list)


# find the email addresses of the target email people
email_links = []
for component in values_list:

    find = wks_2.find(component)
    r, _ = find.row, find.col
    link = empty_string(wks_2.cell(r, 2).value)
    email_links.append(link)

print(email_links)

# send email to multiple accounts
for email in email_links:
    send_email(subject, email, msg)

print("All emails sent")