import datetime

date_time = datetime.datetime.now()

d = date_time.strftime("%m-%d-%Y")
t = date_time.strftime("%H:%M:%S")

print(d)
print("\n")
print(t)
