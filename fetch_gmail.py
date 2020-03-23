#this program produces nicely formated email strings

from ImapClient import ImapClient

import email
import email.header
import imaplib
import os
import sys

from credentials import gmail_password, gmail_user

def main():
    """
    You will need to store your email password in your environment, e.g.
    export mailpwd=password
    """
    imap = ImapClient(recipient=gmail_user)
    imap.login()
    # retrieve messages from a given sender
    messages = imap.get_messages(sender='powerschool@mvsdschools.org')
    # Do something with the messages
    print("Messages in my inbox:")
    for msg in messages:
        # msg is a dict of {'num': num, 'body': body}
        print(msg['num'])
        print(msg['body'])
        # you could delete them after viewing
        # imap.delete_message(msg['num'])
    # when done, you should log out
    imap.logout()


if __name__ == "__main__":
    main()