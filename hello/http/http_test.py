# https://docs.python.org/3/library/json.html
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request as req
import urllib.parse as parse
import sys
import json
from urllib.error import HTTPError

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


class TrelloConfig:
    def __init__(self):

        try:
            with open("config.yml", 'r') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            data_config_trello = cfg['trello']

            self.board_id = '5a569126de60d26499350252'  # Pull requests/Ole
            self.key = data_config_trello['key']
            self.token = data_config_trello['token']

        except:
            print("Something went wrong when writing to the file")

    def __repr__(self):
        return repr((self.board_id, self.key, self.token))


class ResponseApi:
    def __init__(self, json, status, reason):
        self.json = json
        self.status = status
        self.reason = reason

    def __repr__(self):
        return repr((self.json, self.status, self.reason))


def get_json_from_api(api_url, method):
    #print(f'api: {method}', api_url)

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


def find_pr_in_trello(key, token, board_id):
    data_to_search = input('pr number:')
    #data_to_search='119999'
    trello_api = f'https://api.trello.com/1/search?query={parse.quote(data_to_search)}&idBoards={board_id}&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=true&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key={key}&token={token}'
    response = get_json_from_api(trello_api, 'GET')

    if response is not None and response.status == 200 and len(response.json['cards']) > 0:
        print('Good, pr founded in trello board.')

        first_card = response.json['cards'][0]
        print('> first card json', first_card)

        card_id = first_card['id']

        print('> Id:', card_id)
        print('> Name', first_card['name'])

        answer = input('Is it your trello''s card? (Y/N): ')

        if answer.lower() == 'n':
            print('bye, see you again...')
            sys.exit()
        move_pr_trello(card_id, key, token, board_id)

    else:
        print('Sorry, we could not found your PR number in trello, try again.')
        #print('response', response.json)
        #print(response.status)
        #print(response.reason)


def get_valid_numeric_option(max):
    number_template = -1
    while number_template < 0 or number_template > max:
        try:
            number_template = int(input('> '))
        except ValueError as ve:
            print(f'Error: {ve}. Try again...')

    return number_template


def move_pr_trello(trello_card_id, key, token, board_id):

    trello_lists_board_api = f'https://api.trello.com/1/boards/{board_id}/?fields=name&lists=all&list_fields=all'

    response = get_json_from_api(trello_lists_board_api, 'GET')

    total = len(response.json['lists'])

    list_from_boards = response.json['lists']
    print('\nWhich list do you wanna move?')
    for t in range(total):
        print(f"> {t} - {list_from_boards[t]['name']}")

    number_choosed = get_valid_numeric_option(total)

    id_list_to_move = list_from_boards[number_choosed]['id']
    name_list_to_move = list_from_boards[number_choosed]['name']

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


def main():
    config = TrelloConfig()
    find_pr_in_trello(config.key, config.token, config.board_id)


main()
