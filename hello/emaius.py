#import win32com.client
#from win32com.client import Dispatch, constants

# const=win32com.client.constants
# olMailItem = 0x0
# obj = win32com.client.Dispatch("Outlook.Application")
# newMail = obj.CreateItem(olMailItem)
# newMail.Subject = "I AM SUBJECT!!"
#  newMail.Body = "I AM\nTHE BODY MESSAGE!"
# newMail.BodyFormat = 2 # olFormatHTML https://msdn.microsoft.com/en-us/library/office/aa219371(v=office.11).aspx
# newMail.HTMLBody = "<HTML><BODY>Enter the <span style='color:red'>message</span> text here.</BODY></HTML>"
# newMail.To = "allan.barros@gmail.com"
# attachment1 = r"C:\Temp\example.pdf"
# newMail.Attachments.Add(Source=attachment1)
# newMail.display(true)
# newMail.send()


# import win32com.client
# import win32com
# import os
# import sys

# # f = open("testefile.txt","w+")

# outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
# accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts;

# for account in accounts:
#     print(account.DeliveryStore.DisplayName)
# print(accounts);

#####################
# import smtplib

# sendto = 'allan.barros@gmail.com'
# user= 'allan.pedroni@oletecnologia.com'
# password = "p@dron743252"
# smtpsrv = "smtp.office365.com"
# smtpserver = smtplib.SMTP(smtpsrv,587)

# smtpserver.ehlo()
# smtpserver.starttls()
# smtpserver.ehlo
# smtpserver.login(user, password)
# header = 'To:' + sendto + 'n' + 'From: ' + user + 'n' + 'Subject:testing n'
# print(header)
# msgbody = header + 'n This is a test Email send using Python nn'
# smtpserver.sendmail(user, sendto, msgbody)
# print('done!')
# smtpserver.close()
##############
# import os
# import smtplib
# import getpass
# #import mimetypes

# from email.utils import formataddr
# from email.utils import formatdate
# from email.utils import COMMASPACE

# from email.header import Header
# from email import encoders

# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage

# #from O365 import Message

# def send_email(sender_name: str, sender_addr: str, smtp: str, port: str,
#                recipient_addr: list, subject: str, html: str, text: str,
#                img_list: list=[], attachments: list=[],
#                fn: str='last.eml', save: bool=False):

#     passwd = "p@dron743252"

#     sender_name = Header(sender_name, 'utf-8').encode()

#     msg_root = MIMEMultipart('mixed')
#     msg_root['Date'] = formatdate(localtime=1)
#     msg_root['From'] = formataddr((sender_name, sender_addr))
#     msg_root['To'] = COMMASPACE.join(recipient_addr)
#     msg_root['Subject'] = Header(subject, 'utf-8')
#     msg_root.preamble = 'This is a multi-part message in MIME format.'

#     msg_related = MIMEMultipart('related')
#     msg_root.attach(msg_related)

#     msg_alternative = MIMEMultipart('alternative')
#     msg_related.attach(msg_alternative)

#     msg_text = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
#     msg_alternative.attach(msg_text)

#     msg_html = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
#     msg_alternative.attach(msg_html)

#     for i, img in enumerate(img_list):
#         with open(img, 'rb') as fp:
#             msg_image = MIMEImage(fp.read())
#             msg_image.add_header('Content-ID', '<image{}>'.format(i))
#             msg_related.attach(msg_image)

#     for attachment in attachments:
#         fname = os.path.basename(attachment)

#         with open(attachment, 'rb') as f:
#             msg_attach = MIMEBase('application', 'octet-stream')
#             msg_attach.set_payload(f.read())
#             encoders.encode_base64(msg_attach)
#             msg_attach.add_header('Content-Disposition', 'attachment',
#                                   filename=(Header(fname, 'utf-8').encode()))
#             msg_root.attach(msg_attach)

#     mail_server = smtplib.SMTP(smtp, port)
#     mail_server.ehlo()

#     try:
#         mail_server.starttls()
#         mail_server.ehlo()
#     except smtplib.SMTPException as e:
#         print(e)

#     mail_server.login(sender_addr, passwd)
#     mail_server.send_message(msg_root)
#     mail_server.quit()

#     if save:
#         with open(fn, 'w') as f:
#             f.write(msg_root.as_string())


# if __name__ == '__main__':
#     # Usage:
#     sender_name = 'teste'
#     sender_addr = 'allan.pedroni@oletecnologia.com'
#     smtp = 'smtp.office365.com'
#     port = '587'
#     recipient_addr = ['allan.pedroni@oletecnologia.com']
#     subject = 'testandoo'
#     text = "asdasd"
#     html = """
#         <html>
#         <head>
#         <meta http-equiv="content-type" content="text/html;charset=utf-8" />
#         </head>
#         <body>
#         <font face="verdana" size=2>{}<br/></font>
#         <img src="cid:image0" border=0 />
#         </body>
#         </html>
#         """.format(text)  # template
#     img_list = []  # -> image0, image1, image2, ...'python_powered.png'
#     attachments = [] #'załącznik.zip'

#     send_email(sender_name, sender_addr, smtp, port,
#                recipient_addr, subject, html, text,
#                img_list, attachments, fn='my.eml', save=True)