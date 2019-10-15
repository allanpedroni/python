#!/usr/bin/env python

# TODO: search
# - https://docs.python.org/3/library/json.html
# - https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import json
import os
import sys
import urllib.parse as parse
import urllib.request as req
from urllib.error import HTTPError

from colorama import Fore, Back, Style

url = 'http://www.python.org/'


# with req.urlopen(url) as f:
#    print(f.read(300).decode('utf-8'))


# f = req.urlopen(url= url)
# print(f.read().decode('utf-8'))


# TODO: continuar daqui..
# 1- https://www.google.com/search?q=python+use+config+file&rlz=1C1SQJL_enBR856BR856&oq=python+use+config+file&aqs=chrome..69i57.6758j0j7&sourceid=chrome&ie=UTF-8
# 2- yaml file
# https://martin-thoma.com/configuration-files-in-python/
# 3- configparser
# https://docs.python.org/3.4/library/configparser.html


class Board:

    def __init__(self, idBoard):
        self.idBoard = idBoard

    def get_lists(self):
        if self.lists is None:
            self.lists = get_lists_from_board(self.idBoard)
        return self.lists


class TrelloConfig:
    def __init__(self):

        try:
            self.idBoard = os.environ.get('TRELLO_BOARD')
            self.key = os.environ.get('TRELLO_KEY')
            self.token = os.environ.get('TRELLO_TOKEN')

            assert (self.idBoard is not None), "idBoard environment variable is missing."
            assert (self.key is not None), "key environment variable is missing."
            assert (self.token is not None), "token environment variable is missing."

        except Exception as ex:
            message_red_style(f"Something went wrong when reading environment variables. Error: {ex}")
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


def get_json_from_api(api_url, method):

    try:

        f = req.Request(url=api_url, data=None, method=method)

        with req.urlopen(f) as ff:
            json_data_file = ff.read().decode('utf-8')
            return ResponseApi(json.loads(json_data_file), ff.status, ff.reason)
    except HTTPError as ht:
        print('Error:', ht)
        print('Sorry, something wrong happens.')
        sys.exit()

    return None


def find_pr_in_trello(data_to_search, key, token, idBoard):
    trello_api = f'https://api.trello.com/1/search?query={parse.quote(data_to_search)}&idBoards={idBoard}&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=true&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key={key}&token={token}'

    response = get_json_from_api(trello_api, 'GET')

    assert (response is not None), 'Sorry, we could not found your PR number in trello, try again.'
    assert (response.status == 200), message_warning_style(
        'Sorry, there is something wrong with trello api, please try again.')

    if len(response.json['cards']) > 0:
        message_green_style('Good, pr founded in trello board.')

        firstCard = response.json['cards'][0]

        idCard = firstCard['id']
        idList = firstCard['idList']

        listName = get_name_of_list_from_card(idList, idBoard)

        print('> Id\t\t\t:', idCard)
        print('> Name\t\t\t:', firstCard['name'])
        print('> Actual List\t:', listName)

        answer = input('\nIs it your trello\'s card? (Y/N): ')

        if answer.lower() == 'n':
            message_red_style('bye, see you again...')
            sys.exit()
        move_pr_trello(idCard, key, token, idBoard)


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

    choosedNumber = get_valid_numeric_option(total)

    id_list_to_move = jsonLists[choosedNumber]['id']
    name_list_to_move = jsonLists[choosedNumber]['name']

    trello_update_card_api = f'https://api.trello.com/1/cards/{trello_card_id}?idList={id_list_to_move}&key={key}&token={token}'

    response = get_json_from_api(trello_update_card_api, 'PUT')

    assert (response.status == 200), message_red_style('Something wrong happens when moving card...')

    message_warning_style(f'moving card to {name_list_to_move}...')

    new_post = f'AUTOMATICO: Movendo card para {name_list_to_move}'

    trello_add_new_comment = f'https://api.trello.com/1/cards/{trello_card_id}/actions/comments?text={parse.quote(new_post)}&&key={key}&token={token}'
    response = get_json_from_api(trello_add_new_comment, 'POST')

    assert (response.status == 200), message_red_style('Something wrong happens when adding a new comment...')

    message_warning_style('adding new comment...')


def main(use_args):
    pr = 0

    # args
    if use_args:

        total_args = len(sys.argv)
        if total_args == 1:
            print('COMMAND arg1; arg1=pr number;')
            sys.exit()

        pr = sys.argv[1]

    config = TrelloConfig()
    find_pr_in_trello(str(pr), config.key, config.token, config.idBoard)


if __name__ == "__main__":
    try:
        main(use_args=True)
    except Exception as ex:
        print('Error:', ex)
    except:
        pass
