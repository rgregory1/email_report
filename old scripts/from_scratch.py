import imaplib, email
from credentials import gmail_password, gmail_user


# setup varibles
user = gmail_user
password = gmail_password
imap_url = 'imap.gmail.com'

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

# create connections
con = imaplib.IMAP4_SSL(imap_url)
con.login(user,password)
con.select('INBOX')

# test various things to do inside gmail
print(con.list())


# # check specific email
# result, data = con.fetch(b'3','(RFC822)')
# print(data)


# c
result, data = con.fetch(b'3','(RFC822)')
raw = email.message_from_bytes(data[0][1])
print(get_body(raw))