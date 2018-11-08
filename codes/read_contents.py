import gspread
from oauth2client.service_account import ServiceAccountCredentials

# APIs are used
scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# keep secret
cred_file = 'Sheets Test2-316f8201c13e.json'  # --->>>> techacademy1234@gmail.com

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

# authorize
gc = gspread.authorize(credentials)

# open ss
worksheet = gc.open('test')

# main order cart
wks_1 = worksheet.get_worksheet(4)

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


values_list = comp_list(wks_1.col_values(1)[1:])

checker = "14-8-18"

if checker in values_list:
    find = wks_1.find(values_list[values_list.index(checker)])
    r, c = find.row, find.col
    print("Found at %d, %d" %(r, c))







