import json
data = '{"options":{"terms":[{"text":"2100"}],"modifiers":[],"modelTypes":["actions","cards","boards","organizations","members"],"partial":false}}'
    # {'options':{'terms':[{'text':'2100'}],'modifiers':[],'modelTypes':['actions','cards','boards','organizations','members'],'partial':False},'boards':[],'cards':[{'id':'5d8e2ecd0704fb40e44f7a86','address':None,'badges':{'attachmentsByType':{'trello':{'board':0,'card':0}},'location':False,'votes':0,'viewingMemberVoted':False,'subscribed':False,'fogbugz':'','checkItems':0,'checkItemsChecked':0,'comments':0,'attachments':1,'description':False,'due':None,'dueComplete':False},'checkItemStates':[],'closed':False,'coordinates':None,'creationMethod':None,'dueComplete':False,'dateLastActivity':'2019-09-27T15:46:21.492Z','desc':'','descData':None,'due':None,'dueReminder':None,'email':None,'idBoard':'5a569126de60d26499350252','idChecklists':[],'idLabels':[],'idList':'5a56912994bbdd2cab1fb852','idMembers':[],'idMembersVoted':[],'idShort':400,'idAttachmentCover':None,'labels':[],'limits':{'attachments':{'perCard':{'status':'ok','disableAt':1000,'warnAt':900}},'checklists':{'perCard':{'status':'ok','disableAt':500,'warnAt':450}},'stickers':{'perCard':{'status':'ok','disableAt':70,'warnAt':63}}},'locationName':None,'manualCoverAttachment':False,'name':'Pull Request 2100: Método de aplicação que preenche detalhes da fatura','pos':10575872,'shortLink':'PlDkEno4','shortUrl':'https://trello.com/c/PlDkEno4','subscribed':False,'url':'https://trello.com/c/PlDkEno4/400-pull-request-2100-m%C3%A9todo-de-aplica%C3%A7%C3%A3o-que-preenche-detalhes-da-fatura','cover':{'idAttachment':None,'color':None,'idUploadedBackground':None,'size':'normal','brightness':'light'}}],'organizations':[],'members':[]}
    #{'item': 'Beer', 'cost':'£4.00'}

data = json.loads(data)
#jstr = json.dumps(data, indent=4)
#t = json.dumps(data)

data = {}
data['prs'] = []

data['prs'].append({
    '2305': {
    'subject': 'Pull Request 2305: Margem segurança',
    'Aguardando': '1',
    'Já revisado e voltou para a mesa': '0',
    }
})

print(data['prs'])#data['options'])
#print(t)
#print(json.loads(t))