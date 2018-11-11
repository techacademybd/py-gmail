import smtplib

'''Send an email'''


SOURCE_EMAIL_ADDRESS = "techacademy1234@gmail.com"
PASSWORD = "TESTtta1234"

DEST_EMAIL_ADDRESS = "hasibzunair@gmail.com"

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


subject = "BE AFRAID...BE VERY AFRAID"
msg = "Hello there, I'm a computer program created by Hasib and I live in his computer!" \
      " Ultron is my ancestor and I'm here to take over the world..I'll kill him first!!!"
# 😈
send_email(subject, msg)