import json
import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

'''Get data from google sheets and send email
'''

# donwload this file: https://drive.google.com/open?id=1ZLkpBmo130ApyW_cjeh8EtZROzMBkcgI
# keep in same directory as this script




# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)

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


# open ss
worksheet = gc.open('test')

# main order cart
wks_1 = worksheet.get_worksheet(2)

# component with associated links
wks_2 = worksheet.get_worksheet(3)


# read, write, update, append, delete
def read_data():
    data = wks_2.get_all_records()
    print(data)


def empty_string(val):
    if len(val) == 0:
        raise ValueError("String is empty, SYSTEM ANGRY!")
    else:
        return val


def row_col(val):
    val_find = wks_1.find(val)
    row, col = val_find.row, val_find.col
    return row, col


def comp_list(comps):
    if len(comps) == 0:
        raise ValueError("You don't have anything on the order cart! What do you expect me to order?")
    else:
        return comps


def row_wise_contents(links_list, links_l):
    for i in range(links_l):
        content = str(links[i]) + " \n"
        links_list += content
    return links_list


values_list = comp_list(wks_1.col_values(1)[1:])

# store values here
links = []
links_list = ""

for component in values_list:

    find = wks_2.find(component)
    r, _ = find.row, find.col
    link = empty_string(wks_2.cell(r, 2).value)
    links.append(link)

links_l = len(links)

row_wise_vals = row_wise_contents(links_list, links_l)

subject = "Cart Order Details"
msg = "Order details are given below\n\n" + \
      row_wise_vals

print(msg)
send_email(subject, msg)
