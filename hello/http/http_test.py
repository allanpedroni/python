# https://docs.python.org/3/library/json.html
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request as req
import urllib.parse as parse
import sys, json, os
from urllib.error import HTTPError
from trello import TrelloApi
import subprocess

import yaml

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
            with open("config.yml", 'r') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            data_config_trello = cfg['trello']

            self.idBoard = data_config_trello['idBoard']  # Pull requests/Ole
            self.key = data_config_trello['key']
            self.token = data_config_trello['token']

        except Exception as ex:
            print("Something went wrong when reading 'config.yml' file.\nError:", ex)
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


def get_json_from_api(api_url, method):
    # print(f'api: {method}', api_url)

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
    # data_to_search = input('pr number:')
    #data_to_search = '9999'
    trello_api = f'https://api.trello.com/1/search?query={parse.quote(data_to_search)}&idBoards={idBoard}&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=true&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key={key}&token={token}'
    response = get_json_from_api(trello_api, 'GET')

    if response is not None and response.status == 200 and len(response.json['cards']) > 0:
        print('Good, pr founded in trello board.')

        firstCard = response.json['cards'][0]
        #print('> first card json', firstCard)

        idCard = firstCard['id']
        idList = firstCard['idList']
        # print(idList)
        listName = get_name_of_list_from_card(idList, idBoard)

        print('> Id\t\t\t:', idCard)
        print('> Name\t\t\t:', firstCard['name'])
        print('> Actual List\t:', listName)

        answer = input('\nIs it your trello\'s card? (Y/N): ')

        if answer.lower() == 'n':
            print('bye, see you again...')
            sys.exit()
        move_pr_trello(idCard, key, token, idBoard)

    else:
        print('Sorry, we could not found your PR number in trello, try again.')
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

    print('list choosen', id_list_to_move)

    trello_update_card_api = f'https://api.trello.com/1/cards/{trello_card_id}?idList={id_list_to_move}&key={key}&token={token}'

    response = get_json_from_api(trello_update_card_api, 'PUT')

    print(f'moving card to {name_list_to_move}...')
    # print('stat', response.status)
    # print('json', response.json)

    new_post = f'AUTOMATICO: Movendo card para {name_list_to_move}'

    trello_add_new_comment = f'https://api.trello.com/1/cards/{trello_card_id}/actions/comments?text={parse.quote(new_post)}&&key={key}&token={token}'
    response = get_json_from_api(trello_add_new_comment, 'POST')
    print('adding new comment...')
    # print('stat', response.status)
    # print('json', response.json)


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

def testUsingNewApiTrello():
    # trello = TrelloApi('')
    # https://pypi.org/project/trello/
    # https: // pythonhosted.org / trello / examples.html
    # print(os.environ["TRELLO_KEY"])

    config = TrelloConfig()
    tre = TrelloApi(config.key, config.token)

    #print('t:',tre.boards.get_card(config.idBoard))
    print('a:', tre.boards.get_action(config.idBoard))
    print('x:', tre.boards.get_list(config.idBoard))



if __name__ == "__main__":
    #main(use_args=True)
    testUsingNewApiTrello()

