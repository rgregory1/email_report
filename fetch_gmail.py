#this program produces nicely formated email strings

from ImapClient import ImapClient

import email
import email.header
import imaplib
import os
import sys

from credentials import gmail_password, gmail_user, me

import yagmail





def main():
    
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

    messages_2 = imap.get_messages(sender='no_reply@pcgus.com')


    imap.logout()

    # process vcat raw message in to three seperate lines
    for dic in messages:
        dic['body']=dic['body'].replace('\r','')
        dic['body']=dic['body'].replace('\n\n','\n')
        dic['body']=dic['body'].split('\n')

    # find line with success in it and bold it
    for dic in messages:
        # if 'VCAT' in dic['body'][0]:
        for count,string in enumerate(dic['body'],0):
            if 'successful' in string:
                dic['body'][count] = '<b>' + string + '</b>'




    # prepare variable for sending
    contents = []

    # add VCAT messages to contents
    for msg in messages:
        for line in msg['body']:
            contents.append(line)
        contents.append('\n<hr>\n')
    for msg in messages_2:
        contents.append(msg['body'])

    yag = yagmail.SMTP(gmail_user, gmail_password)

    # contents = [
    #     "This is the body, and here is just text http://somedomain/image.png",
    #     "You can find an audio file attached.", '/local/path/to/song.mp3'
    # ]
    yag.send(me, 'PS Report Summary', contents)


if __name__ == "__main__":
    main()