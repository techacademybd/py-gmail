import datetime
import os


'''Triggers the post-email.py script in the given time
'''

# input time in hours, minutes and seconds...
checker = "15:14:30"

while 1:
    date_time = datetime.datetime.now()
    d = date_time.strftime("%m-%d-%Y")
    t = date_time.strftime("%H:%M:%S")

    if t == checker:
        print("Starting new script....")
        os.system("post-email.py 1")
        break
