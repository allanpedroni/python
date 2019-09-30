# https://docs.python.org/3/library/json.html
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request as req
import urllib.parse as parse
import sys
import json
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

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

data_config_trello = cfg['trello']

board = '5a569126de60d26499350252'  # Pull requests/Ole
key = data_config_trello['key']
token = data_config_trello['token']


def find_pr_in_trello(key, token):
    data_to_search = input('pr number:')
    # data=9999
    trello_api = f'https://api.trello.com/1/search?query={parse.quote(data_to_search)}&idBoards={board}&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=true&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key={key}&token={token}'
    print('api:', trello_api)
    f = req.Request(url=trello_api, data=None, method='GET')

    with req.urlopen(f) as ff:
        json_data_file = ff.read().decode('utf-8')
        json_from_pr = json.loads(json_data_file)

    # data = {'people':[{'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'}]}
    # json.dumps(data, sort_keys=True, indent=4)

    id_list_to_move = '5a569160ba8256f35d201a3a'

    if ff.status == 200 and len(json_from_pr['cards']) > 0:
        print('trello pr founded.')
        print(json_from_pr)

        primeiro_card = json_from_pr['cards'][0]
        print('primeiro_card', primeiro_card)
        trello_card_id = primeiro_card['id']
        print('> Id:', trello_card_id)
        print('> Name', primeiro_card['name'])

        move_pr_trello(trello_card_id, id_list_to_move, key, token)

    else:
        print('trello pr NOT found.')
        print('response', json_data_file)
        print(ff.status)
        print(ff.reason)


def get_valid_numeric_option():
    number_template=-1
    while number_template < 0 or number_template > 4:
        try:
            number_template = int(input('> '))
        except ValueError as ve:
            print(f'Error: {ve}. Try again...')

    return number_template


def move_pr_trello(trello_card_id, id_list_to_move, key, token):

    templates = [f'Move to \'Aguardando\'.',
                 f'Move to \'Em andamento\'.',
                 f'Move to \'Já revisado e voltou para a mesa\'.',
                 f'Move to \'Revisão\'.',
                 f'Move to \'Finalizado\'.']
    for c in range(4):
        print(f'{c}-{templates[c]}')

    option= get_valid_numeric_option()

    print('option choosen', option)
    sys.exit()
    answer = input('mudar para finalizado?')
    if answer.lower() == 'y':
        trello_update_card_api = f'https://api.trello.com/1/cards/{trello_card_id}?idList={id_list_to_move}&key={key}&token={token}'

        put_request = req.Request(url=trello_update_card_api, data=None, method='PUT')
        print('moving card to finalizando...')
        with req.urlopen(put_request) as pr:
            print(pr.read())
            print(pr.status)
            print(pr.reason)


def main():
    find_pr_in_trello(key, token)


main()
