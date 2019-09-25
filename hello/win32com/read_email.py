#!/usr/bin/env python

import sys
from colorama import Fore, Back, Style


class message_email:
    def __init__(self, pr, message):
        self.pr = pr
        self.subject = message.Subject
        self.date = message.SentOn
        self.fromm = message.SenderName
        self.to = message.To
        self.message = message

    def __repr__(self):
        return repr((self.pr, self.subject, self.date, self.message))


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

        question = '\n# select the template number:'
        print(question)
        templates = [f'PR {pr_number} verificado, favor verificar os comentários.',
                     f'PR {pr_number} aprovado e completado.',
                     f'Aprovei o PR {pr_number} com sugestões e configurado auto-complete (pendente voto da mesa para completar).',
                     f'PR {pr_number} aprovado e configurado auto-complete (pendente voto da mesa para completar).',
                     f'Sair.']
        for c in range(5):
            print(f'{c}- {templates[c]}')

        number_template = -1

        while number_template < 0 or number_template > 4:
            try:
                number_template = int(input('> '))
            except ValueError as ve:
                print(f'Error: {ve}')

        if number_template == 4:
            print('bye...')
            sys.exit()

        return templates[number_template]

    @staticmethod
    def get_emails_from_pr(pr):

        import win32com.client as win32
        import re

        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

        emails = []

        try:
            box = outlook.GetDefaultFolder(6)  # caixa de Entrada

            messages = box.Items

            messages.Sort("[ReceivedTime]", True)

            for item in messages:

                founds = re.findall(rf'{pr}', item.Subject, re.MULTILINE)

                total_emails_found = len(founds)

                if total_emails_found == 0:  # first search in body email
                    founds = re.findall(rf'{pr}', item.Body, re.MULTILINE)
                    total_emails_found = len(founds)

                if total_emails_found >= 1:
                    emails.append(message_email(pr, item))
        except:
            pass

        emails_sorted = sorted(emails, key=lambda message_email: message_email.date, reverse=True)

        message_green_style(f'({len(emails_sorted)}) email found.')

        for e in emails_sorted:
            print('> Sent On:', e.date, '\t', e.subject)

        return emails_sorted[0]


def send_email(message: message_email, template_email, force_to_send=False):
    senderName = message.fromm.split(' ')

    if len(senderName) > 0:
        first_name = senderName[0]

    answer = f'{first_name.capitalize()}, <br /><br />{template_email}<br /><br />Att'

    reply = message.message.ReplyAll()
    reply.HTMLBody = answer + reply.HTMLBody

    if force_to_send:
        reply.Send()
    else:
        reply.Display(True)


def verify_email(message: message_email):
    message_red_style('Confirm this email?')
    print('\nTo     : {to}\nFrom   : {fromm}\nSubject: {subject},\nLast date : {'
          'date}\n=============\n '
          .format(to=message.to, fromm=message.fromm, subject=message.subject, date=message.date))

    response = input('> (Y/N)? ')

    return response.lower() == 'y'


def message_red_style(text):
    print('\n' + Back.RED + Fore.LIGHTWHITE_EX +
          text +
          Style.RESET_ALL)


def message_green_style(text):
    print('\n' + Back.LIGHTGREEN_EX + Fore.BLACK +
          text +
          Style.RESET_ALL)


def main(use_args):
    pr = 0
    send_email_directly = False

    # args
    if use_args:

        total_args = len(sys.argv)
        if total_args == 1:
            print('COMMAND arg1 arg2; arg1=pr number; arg2= (OPTIONAL) force to send email')
            sys.exit()

        pr = sys.argv[1]

        if total_args > 2:
            send_email_directly = sys.argv[2]

    message_red_style(f'Config:')
    print(f'\n> Args:{sys.argv.__str__()}'
          f'\n> PR number:{pr}'
          f'\n> Send email automatically:{send_email_directly}')

    message_red_style('1- get emails template..')
    template = PR.get_resolution_template_email(pr)

    message_red_style('2- searching email..')
    email_message = PR.get_emails_from_pr(pr)

    if email_message is None:
        print('bye...')
    else:
        send_email_answer_yes = verify_email(email_message)

        if send_email_answer_yes:
            message_red_style('sending email..')
            # send_email(message=email_message, template_email=template, force_to_send=send_email_directly)
        else:
            print('bye...')

    sys.exit()


if __name__ == "__main__":
    main(use_args=True)

# se template 0 - verificar template
# mover PR para quadro 'Já revisado e voltou para a mesa'
# se template 1, 2 ou 3 - aprovado
# mover PR para Finalizado
# incluir template para sair do programa
