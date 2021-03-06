# this program produces nicely formated email strings

from ImapClient import ImapClient

import datetime
import email
import email.header
import imaplib
import os
import sys
import pathlib
from credentials import gmail_password, gmail_user, me

import yagmail


def main():

    # set snap_text variable so it doesn't break progam if not present
    snap_txt = ""

    # get timestamp for log
    temp_timestamp = str(datetime.datetime.now())
    print("\n\n" + temp_timestamp)
    print("------------------------------\n")
    today = temp_timestamp.split()[0]

    imap = ImapClient(recipient=gmail_user)
    imap.login()

    def remove_messages_from_sender(current_messages):
        for msg in current_messages[::-1]:
            # msg is a dict of {'num': num, 'body': body}
            # print(msg["num"])
            # print(msg["subject"])
            # print(msg["body"])
            # you could delete them after viewing
            imap.delete_message(msg["num"])

    # retrieve powerschool messages
    ps_messages = imap.get_messages(sender="powerschool@mvsdschools.org")
    # remove messages from ps from inbox
    remove_messages_from_sender(ps_messages)

    gv_messages = imap.get_messages(sender="no_reply@pcgus.com")
    # remove messages from goalview from inbox
    remove_messages_from_sender(gv_messages)

    snap_messages = imap.get_messages(
        sender="HostedImport@hosting.snaphealthcenter.com"
    )
    # remove messages from snap from inbox
    remove_messages_from_sender(snap_messages)

    # when done, you should log out
    imap.logout()

    # process vcat raw message in to three seperate lines
    for dic in ps_messages:
        dic["body"] = dic["body"].replace("\r", "")
        dic["body"] = dic["body"].replace("\n\n", "\n")
        dic["body"] = dic["body"].split("\n")

    # find line with success in it and bold it
    for dic in ps_messages:
        # if 'VCAT' in dic['body'][0]:
        for count, string in enumerate(dic["body"], 0):
            if "successful" in string:
                dic["body"][count] = "<b>" + string + "</b>"

    # find the snap report txt file
    attachment_folder = pathlib.Path.cwd().joinpath("attachments")
    files_in_basepath = attachment_folder.iterdir()
    for item in files_in_basepath:
        if item.suffix == ".txt":
            print(item.name)
            snap_txt = item

    # read the txt file to a list
    # if "snap_text" in locals():
    if snap_txt != "":
        with open(snap_txt) as f:
            snap_report = f.readlines()

        # add info to identify information
        snap_report.insert(0, "SNAP Report")
        snap_txt.unlink()

    # prepare variable for sending
    contents = []

    # add VCAT messages to contents
    for msg in ps_messages:
        for line in msg["body"]:
            contents.append(line)
        contents.append("\n<hr>\n")

    for msg in gv_messages:
        contents.append(msg["body"])

    if "snap_report" in locals():
        # add seperator to end of goalview info
        contents.append("\n<hr>\n")
        for msg in snap_report:
            contents.append(msg)

    yag = yagmail.SMTP(gmail_user, gmail_password)

    if len(contents) == 0:
        contents = "No emails today"

    # contents = [
    #     "This is the body, and here is just text http://somedomain/image.png",
    #     "You can find an audio file attached.", '/local/path/to/song.mp3'
    # ]
    yag.send(me, "PS Report Summary " + today, contents)


if __name__ == "__main__":
    main()
