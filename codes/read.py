import imaplib
import email

'''Read the latest email in the inbox
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
email_message = email.message_from_string(raw_email)

# convert raw email to text
message = get_first_text_block(email_message)

print("Sent from: " + str(email.utils.parseaddr(email_message['From'])[0]))
print("\n")
print("Email subject: " + str(email_message['Subject']))
print("\n")
print("Message: " + str(message))
