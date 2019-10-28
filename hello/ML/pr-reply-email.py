#!/usr/bin/env python

# TODO:
#  1- if template 1,2,3 -> MOVE to Finished in trello
#  2- if template 0 -> MOVE to Already reviewed in trello

import json
import os
import sys
import urllib.parse as parse
import urllib.request as req
from string import Template
from urllib.error import HTTPError
import win32com.client as win32
import re
import csv, datetime


class EmailMessage:
    def __init__(self, message, urls):
        self.subject = message.Subject
        self.date = message.SentOn.strftime("%m/%d/%Y %H:%M:%S")
        self.fromm = message.SenderName
        self.to = message.To
        self.urls = urls

    def __repr__(self):
        return repr((self.subject, self.date, self.fromm, self.to, self.urls))


def main(use_args):
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")


    emails = []

    try:
        box = outlook.GetDefaultFolder(6)  # caixa de Entrada

        messages = box.Items

        messages.Sort("[ReceivedTime]", True)

        for item in messages:

            urls = re.findall(
                'http[s]?://[www]?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))[^\>]+',
                item.Body)
            #    for url in urls:
            #        t = re.findall(rf'{pr}', url)
            #        if len(t) > 0:
            #            emails.append(EmailMessage(pr, item, url, ''))

            # print('Subject:', item.Subject)
            # print('urls:', urls)
            email = EmailMessage(item, urls)

            emails.append(json.dumps(email.__dict__).replace("\"","\'"))
            #print(email.date)
            #print(email)
            #print('email', json.dumps(email.__dict__))
            #print('email', email)
            #s = json.dumps(email.__dict__)
            #print(s)

            # print('LastModificationTime:', item.LastModificationTime)
            # print('To:', item.To)
            # print('From:', item.SenderName)
            # print('Body:', item.Body.encode("utf-8"))

    except Exception as ex:
        print('Error:', ex)

    #dt = {}
    #dt.update()

    #print(json.loads(json.dumps(emails[0].__dict__)))

    print(emails)

    #with open('data.txt', 'w') as outfile:
        #json.dump(emails, outfile)


    # with open('names.csv', 'w', newline='') as csvfile:
     #    fieldnames = ['subject', 'date', 'fromm', 'to', 'urls']
      #  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader()
        # for e in emails:
         #    print(e.subject)
            #j = json.dumps(e.__dict__)
            #print(j)
            #writer.writerow()
        #writer.writerow({'subject': 'Lovely', 'date': 'Spam'})
        #writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    sys.exit()


if __name__ == "__main__":
    try:
        main(use_args=True)
    except Exception as ex:
        print('Error:', ex)
    except:
        pass
