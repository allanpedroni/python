#!/usr/bin/env python

import sys


class Emails:
    def __init__(self, pr, subject, to, fromm, body):
        self.pr = pr
        self.subject = subject
        self.to = to
        self.fromm = fromm
        self.body = body

    def length_pr(self):
        return len(str(self.pr))

    def is_there_pr_in_subject(self):
        import re
        founds = re.findall(r'\d{self.length_pr()}', self.subject, re.MULTILINE)
        return founds.count() > 0

    def is_there_pr_in_body(self):
        import re
        founds = re.findall(r'\d{self.length_pr()}', self.body, re.MULTILINE)
        return founds.count() > 0


class PR:
    @staticmethod
    def get_pr_number():
        pr = 0
        while pr == 0:
            try:
                pr = int(input('# type the pull request number: '))
            except ValueError as ve:
                print(f'Error: {ve}')
        return pr

    @staticmethod
    def get_resolution_template_email(pr_number):

        question = '# select the template number:'
        print(question)
        templates = [f'PR {pr_number} verificado, favor verificar os comentários.',
                     f'PR {pr_number} aprovado e completado.',
                     f'Aprovei o PR {pr_number} com sugestões e configurado auto-complete (pendente voto da mesa para completar).',
                     f'PR {pr_number} aprovado e configurado auto-complete (pendente voto da mesa para completar).']
        for c in range(4):
            print(f'{c}-{templates[c]}')

        number_template = -1

        while number_template < 0 or number_template > 4:
            try:
                number_template = int(input('> '))
            except ValueError as ve:
                print(f'Error: {ve}')

        # print('template selected:', templates[number_template])
        return templates[number_template]

    @staticmethod
    def get_emails_from_pr(pr):

        import win32com.client as win32
        import re
        # from email.parser import Parser

        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        # https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook
        # https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.outlook.mailitem?redirectedfrom=MSDN&view=outlook-pia#properties_
        # https://www.google.com/search?q=win32com.client.Dispatch(%22Outlook.Application%22)&rlz=1C1SQJL_enBR856BR856&oq=win32com.client.Dispatch(%22Outlook.Application%22)&aqs=chrome..69i57.856j0j7&sourceid=chrome&ie=UTF-8
        # https://pbpython.com/windows-com.html

        emails = []
        # for i in range(50):
        try:
            box = outlook.GetDefaultFolder(6)  # caixa de Entrada

            for item in box.Items:

                # print('Subject:', item.Subject)
                # print('LastModificationTime:', item.LastModificationTime)
                # print('To:', item.To)
                # print('From:', item.SenderName)
                # print('Body:', item.Body.encode("utf-8"))
                # print('------')

                founds = re.findall(rf'{pr}', item.Subject, re.MULTILINE)

                total_emails_found = len(founds)

                if total_emails_found == 0:  # first search in body email
                    founds = re.findall(rf'{pr}', item.Body, re.MULTILINE)
                    total_emails_found = len(founds)

                if total_emails_found == 1:
                    print(f'({total_emails_found}) email found.\n')

                    # print('encode', item.Body)
                    # saving email
                    ##item.SaveAs('c:\\temp\\teste1.msg')

                    # email = Emails(pr, item.Subject, item.To, item.SenderName, item.Body)
                    # emails.append(email)
                    return item
                    # print(item.SenderName.split(' ')[0])
                if total_emails_found > 1:
                    print(f'({total_emails_found}) emails found.')
                    print('under construction')
                    print('Subject of last element.', item[-1].Subject)
                    print('SentOn of last element.', item[-1].SentOn)
                    # return item[-1]  # return the last element of list
                    return None
            # name = box.Name
            # print(6, name)
        except:
            pass
        return None


def send_email(message, template_email, force_to_send=False):
    fromm = message.SenderName.split(' ')

    if len(fromm) > 0:
        first_name = fromm[0]

    # print('BodyFormat',message.HTMLBody)

    reply = message.ReplyAll()

    answer = f'{first_name.capitalize()}, <br /><br />{template_email}<br /><br />Att'
    # reply.body = f'{first_name.capitalize()},\n\n{template_email}\n\nAtt {reply.body}'
    # reply.BodyFormat = 2
    reply.HTMLBody = answer + reply.HTMLBody
    # reply.Display(True)

    if force_to_send:
        reply.Send()
    else:
        reply.Display(True)


def verify_email(message):
    print('=============\nEmails details:\nTo     : {to}\nFrom   : {fromm}\nSubject: {subject},\nSentOn : {'
          'sentwhen}\n============= '
        .format(
        to=message.To,
        fromm=message.SenderName,
        subject=message.Subject,
        sentwhen=message.SentOn))

    response = input('is it your right email (Y/N)? ')

    return response.lower() == 'y'


def main(use_args):
    pr = 0
    send_email_directly = False

    if use_args:
        total_args = len(sys.argv)
        if total_args == 1:
            print('COMMAND arg1 arg2; arg1=pr number; arg2= (OPTIONAL) force to send email')
            sys.exit()

        pr = sys.argv[1]

        if total_args > 2:
            send_email_directly = sys.argv[2]

    template = PR.get_resolution_template_email(pr)
    print('searching email..')
    email_message = PR.get_emails_from_pr(pr)

    if (email_message == None):
        print('bye...')
    else:
        send_email_answer_yes = verify_email(email_message)

        if send_email_answer_yes:
            print('sending email..')
            send_email(message=email_message, template_email=template, force_to_send=send_email_directly)
        else:
            print('bye...')

    sys.exit()


if __name__ == "__main__":
    main(use_args=False)
    # print(len(str(1234)))
    # pr = PR.get_pr_number()
    ##pr = 3430
    ##template = PR.get_resolution_template_email(pr)
    # print(f'PR number:', pr)
    ##email_message = PR.get_emails_from_pr(pr)
    ##send_email(message=email_message, template_email=template, send=False)
    # for e in es:
    #    print(e.subject)

    # sFilter = "[Subject] = 'PR 1856'"
    # message = messages.find(sFilter)
    # body_content = message.body
    # print(body_content)

    # for i in range(50):
    #    try:
    #        box = outlook.GetDefaultFolder(i)
    #        name = box.Name
    #       print(i, name)
    #   except:
    #       pass

    # print(options)
    # pr = get_pr_number()  # pr number
    # get_template_email()
    # while pr == 0:
    #    print('pr invalid!', pr)
    #    pr = get_pr_number()

# print('older')

# try:

# except  as e:
#     print(f'Erro: {e}')
# else:
#     pass
# finally:
#     pass
# https://towardsdatascience.com/log-book-guide-to-excel-outlook-email-delivery-automation-via-python-ca905cbf3f89
