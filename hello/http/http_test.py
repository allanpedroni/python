# https://docs.python.org/3/library/json.html
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request as req
import sys
import json

url = 'http://www.python.org/'

# with req.urlopen(url) as f:
#    print(f.read(300).decode('utf-8'))


#f = req.urlopen(url= url)
#print(f.read().decode('utf-8'))


# TODO: continuar daqui..
#1- https://www.google.com/search?q=python+use+config+file&rlz=1C1SQJL_enBR856BR856&oq=python+use+config+file&aqs=chrome..69i57.6758j0j7&sourceid=chrome&ie=UTF-8
#2- yaml file
# https://martin-thoma.com/configuration-files-in-python/
#3- configparser
# https://docs.python.org/3.4/library/configparser.html


#data = input('pr:')
data=9999
trello_api = f'https://api.trello.com/1/search?query={data}&idBoards=5a569126de60d26499350252&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=false&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key=20446b93c0049d6cd017f362e61dc9bf&token=25f0ff4bd7ca4ff00987f9d200517b908e8282c0c616bc20ffe9a6d3aad0961e'
print('api:',trello_api)
f = req.Request(url= trello_api, data=None, method='GET')

with req.urlopen(f) as ff:
    #print(ff.read().decode('utf-8'))
    #with open(ff.read().decode('utf-8')) as json_data_file:
    json_data_file = ff.read().decode('utf-8')
    #data = {'people': [{'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'}]}
    json_from_pr = json.loads(json_data_file)

#data = {'people':[{'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'}]}
#json.dumps(data, sort_keys=True, indent=4)

id_quadro_finalizado = '5a569160ba8256f35d201a3a'

if ff.status == 200:
    print('trello pr founded.')
    print(json_from_pr)
    trello_card_id = json_from_pr['cards'][0]['id']
    print('> id:', trello_card_id)


trello_update_card_api = f'https://api.trello.com/1/cards/{trello_card_id}?idList={id_quadro_finalizado}&key=20446b93c0049d6cd017f362e61dc9bf&token=25f0ff4bd7ca4ff00987f9d200517b908e8282c0c616bc20ffe9a6d3aad0961e'
print(trello_update_card_api)
print(ff.status)
print(ff.reason)