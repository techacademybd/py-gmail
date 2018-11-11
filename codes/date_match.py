import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

'''This script takes the current date and matches it with a column of dates
in the spreadsheet. Returns the row and column number if found.
'''



# run these before running the script
# pip install gspread
# pip install --upgrade google-api-python-client oauth2client


# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)

# open ss
worksheet = gc.open('test')

# sheet 5
wks_1 = worksheet.get_worksheet(4)


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

def format_date(date):
    return date[:3] + date[4:6] + date[8:]

# get all values in the column
values_list = comp_list(wks_1.col_values(1)[1:])

# get datetime
print("Getting today's date....")
date_time = datetime.datetime.now()
checker = date_time.strftime("%m-%d-%Y")

# get todays date
checker = format_date(checker)

# check if date is in the spreadsheet column
if checker in values_list:
    find = wks_1.find(values_list[values_list.index(checker)])
    r, c = find.row, find.col
    print("Date at (row,column) --> %d, %d" %(r, c))
else:
    print("Not found.. :(")