# https://docs.python.org/3/library/json.html
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request as req
import sys

url = 'http://www.python.org/'

# with req.urlopen(url) as f:
#    print(f.read(300).decode('utf-8'))


#f = req.urlopen(url= url)
#print(f.read().decode('utf-8'))



data = input('pr:')
trello_api = f'https://api.trello.com/1/search?query={data}&idBoards=5a569126de60d26499350252&modelTypes=all&board_fields=name%2CidOrganization&boards_limit=10&card_fields=all&cards_limit=10&cards_page=0&card_board=false&card_list=false&card_members=false&card_stickers=false&card_attachments=false&organization_fields=name%2CdisplayName&organizations_limit=10&member_fields=avatarHash%2CfullName%2Cinitials%2Cusername%2Cconfirmed&members_limit=10&partial=false&key=20446b93c0049d6cd017f362e61dc9bf&token=25f0ff4bd7ca4ff00987f9d200517b908e8282c0c616bc20ffe9a6d3aad0961e'
print('api:',trello_api)
f = req.Request(url= trello_api, data=None, method='GET')

with req.urlopen(f) as ff:
    print(ff.read())
print(ff.status)
print(ff.reason)