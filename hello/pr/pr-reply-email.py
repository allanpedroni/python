#!/usr/bin/env python

# TODO:
#  1- if template 1,2,3 -> MOVE to Finished in trello
#  2- if template 0 -> MOVE to Already reviewed in trello

import json
import os
import sys
import urllib.parse as parse
import urllib.request as req
from urllib.error import HTTPError
from string import Template
from colorama import Fore, Back, Style


class TrelloConfig:
    def __init__(self):

        try:
            # with open("config.yml", 'r') as ymlfile:
            #    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # data_config_trello = cfg['trello']

            self.idBoard = os.environ.get('TRELLO_BOARD')  # data_config_trello['idBoard']  # Pull requests/Ole
            self.key = os.environ.get('TRELLO_KEY')  # data_config_trello['key']
            self.token = os.environ.get('TRELLO_TOKEN')  # data_config_trello['token']

            assert (self.idBoard is not None) # , "idBoard environment variable is missing."
            assert (self.key is not None) # , "key environment variable is missing."
            assert (self.token is not None) # , "token environment variable is missing."

        except Exception as ex:
            print("Something went wrong when reading environment variables. \n"
                  "Please check TRELLO_BOARD, TRELLO_KEY and TRELLO_TOKEN.\nError:", ex)
            sys.exit()

    def __repr__(self):
        return repr((self.idBoard, self.key, self.token))


class ResponseApi:
    def __init__(self, json, status, reason):
        self.json = json
        self.status = status
        self.reason = reason

    def __repr__(self):
        return repr((self.json, self.status, self.reason))


class EmailMessage:
    def __init__(self, pr, message, url, templateEmail):
        self.pr = pr
        self.subject = message.Subject
        self.date = message.SentOn
        self.fromm = message.SenderName
        self.to = message.To
        self.message = message
        self.url = url
        self.templateEmail = templateEmail

    def __repr__(self):
        return repr((self.pr, self.subject, self.date, self.message, self.url))


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

                    urls = re.findall(
                        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))[^\>]+',
                        item.Body)
                    for url in urls:
                        t = re.findall(rf'{pr}', url)
                        if len(t) > 0:
                            emails.append(EmailMessage(pr, item, url, ''))

        except Exception as ex:
            print('Error:', ex)
            sys.exit()

        emails_sorted = sorted(emails, key=lambda EmailMessage: EmailMessage.date, reverse=True)

        message_green_style(f'({len(emails_sorted)}) email found.')

        for e in emails_sorted:
            print('>>>>>>>>>>> Sent On:', e.date, '\t', e.subject, '\n')

        if len(emails_sorted) > 0:
            return emails_sorted[0]
        else:
            return None


def get_json_from_api(api_url, method):
    # print(f'api: {method}', api_url)

    try:

        f = req.Request(url=api_url, data=None, method=method)

        with req.urlopen(f) as ff:
            json_data_file = ff.read().decode('utf-8')
            return ResponseApi(json.loads(json_data_file), ff.status, ff.reason)
    except HTTPError as ht:
        print(f'Url: {api_url}\nSorry, something wrong happens.\n see error:', ht)
        sys.exit()

    return None


def find_pr_in_trello(data_to_search, key, token, idBoard):
    trello_api = f'https://api.trello.com/1/search?query={parse.quote(data_to_search)}&idBoards={idBoard}&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=true&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key={key}&token={token}'

    response = get_json_from_api(trello_api, 'GET')

    if response is not None and response.status == 200 and len(response.json['cards']) > 0:
        message_green_style('Good, pr founded in trello board.')

        firstCard = response.json['cards'][0]
        # print('> first card json', firstCard)

        idCard = firstCard['id']
        idList = firstCard['idList']
        # print(idList)
        listName = get_name_of_list_from_card(idList, idBoard)

        print('> Id\t\t\t:', idCard)
        print('> Name\t\t\t:', firstCard['name'])
        print('> Actual List\t:', listName)

        answer = input('\nIs it your trello\'s card? (Y/N): ')

        if answer.lower() == 'n':
            message_red_style('bye, see you again...')
            sys.exit()
        move_pr_trello(idCard, key, token, idBoard)

    else:
        message_red_style('Sorry, we could not found your PR number in trello, try again.')
        # print('response', response.json)
        # print(response.status)
        # print(response.reason)


def get_valid_numeric_option(max):
    number_template = -1
    while number_template < 0 or number_template > max:
        try:
            number_template = int(input('> '))
        except ValueError as ve:
            print(f'Error: {ve}. Try again...')

    return number_template


def get_lists_from_board(idBoard):
    trello_lists_board_api = f'https://api.trello.com/1/boards/{idBoard}/?fields=name&lists=all&list_fields=all'

    response = get_json_from_api(trello_lists_board_api, 'GET')

    if response is not None and len(response.json['lists']) > 0:
        return response.json['lists']
    return None


def get_name_of_list_from_card(idList, idBoard):
    lists_from_board = get_lists_from_board(idBoard)

    for row in lists_from_board:
        if row['id'] == idList:
            return row['name']
    return None


def move_pr_trello(trello_card_id, key, token, idBoard):
    jsonLists = get_lists_from_board(idBoard)

    total = len(jsonLists)

    print('\nWhich list do you wanna move?')
    for t in range(total):
        print(f"> {t} - {jsonLists[t]['name']} - {jsonLists[t]['id']}")

    number_choosed = get_valid_numeric_option(total)

    id_list_to_move = jsonLists[number_choosed]['id']
    name_list_to_move = jsonLists[number_choosed]['name']

    trello_update_card_api = f'https://api.trello.com/1/cards/{trello_card_id}?idList={id_list_to_move}&key={key}&token={token}'

    response = get_json_from_api(trello_update_card_api, 'PUT')

    message_warning_style(f'moving card to {name_list_to_move}...')
    # print('stat', response.status)
    # print('json', response.json)

    new_post = f'AUTOMATICO: Movendo card para {name_list_to_move}'

    trello_add_new_comment = f'https://api.trello.com/1/cards/{trello_card_id}/actions/comments?text={parse.quote(new_post)}&&key={key}&token={token}'
    response = get_json_from_api(trello_add_new_comment, 'POST')
    message_warning_style('adding new comment...')
    # print('stat', response.status)
    # print('json', response.json)


def send_email(message: EmailMessage, template_email, force_to_send=False):
    senderName = message.fromm.split(' ')

    if len(senderName) > 0:
        first_name = senderName[0]

    template = Template("<div style='font-family: Calibri; font-size: 15px;'>$firstName, <br /><br />"
                        "<a href=$messageUrl>PR $messagePr</a> "
                        "$emailMessage <br /><br />"
                        "Att</div>")

    answer = template.substitute(
        firstName = first_name.capitalize(),
        messageUrl = message.url,
        messagePr = message.pr,
        emailMessage = template_email.replace(f'PR {message.pr}', '')
    )

    reply = message.message.ReplyAll()
    reply.HTMLBody = answer + reply.HTMLBody

    if force_to_send:
        reply.Send()
    else:
        teste = reply.Display(True)


def verify_email(message: EmailMessage):
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


def message_warning_style(text):
    print('\n' + Back.LIGHTYELLOW_EX + Fore.BLACK +
          text +
          Style.RESET_ALL)


def message_green_style(text):
    print('\n' + Back.LIGHTGREEN_EX + Fore.BLACK +
          text +
          Style.RESET_ALL)


def moving_pr_trello(pr):
    config = TrelloConfig()
    find_pr_in_trello(str(pr), config.key, config.token, config.idBoard)


def main(use_args):
    pr = 999999999999999
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

    message_red_style('1- searching email..')
    email_message = PR.get_emails_from_pr(pr)

    if email_message is None:
        print(f'\nSorry but we didnt find any email with {pr}.')
        answer = input('\nDo you wanna move PR in trello? (Y/N) ')

        if answer.lower() == 'y':
            moving_pr_trello(pr)
        else:
            message_red_style('See you next time...')
    else:
        message_red_style('2- get emails template..')
        template = PR.get_resolution_template_email(pr)

        email_message.template = template;

        send_email_answer_yes = verify_email(email_message)

        if send_email_answer_yes:
            message_red_style('3- sending email..')
            send_email(message=email_message, template_email=template, force_to_send=send_email_directly)

            message_red_style('4- moving in trello..')
            moving_pr_trello(pr)
        else:
            print('bye...')

    sys.exit()


if __name__ == "__main__":
    main(use_args=False)
