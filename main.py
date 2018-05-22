from google.cloud import language
from google.cloud.language import types
from google.cloud.language import enums

import argparse
import json
import urllib
import six
import sys

''' This is using Google NLP API'''

def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities
    print entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    all_entities={}
    all_entities['entities']=[]

    for entity in entities:

        if knowledge_graph_entries(entity.name)!={}:
            all_entities['entities'].append(knowledge_graph_entries(entity.name)) #,entity.metadata["mid"])
        else:
            all_entities['entities'].append({'name':entity.name,'type':entity_type[entity.type]})

    return all_entities

#entities_text(query)

def knowledge_graph_entries(query):#,id):

    '''This is using Google Knowledge Graph API'''

    api_key = 'AIzaSyDrQNV9Mb8uS19YHaVM8kNuWgvYu32JlBs'

    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        #'ids':id,
        'limit': 1,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    print response
    d={}
    for element in response['itemListElement']:
        try:
            #print element['result']['name'] + ' (' + str(element['resultScore']) + ')'+' : '+element['result']['detailedDescription']['url']
            d={'name':element['result']['name'],'type':element['result']['@type'],
                'description':element['result']['detailedDescription']['articleBody'],
                'url':element['result']['detailedDescription']['url']}
        except KeyError:
            #print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
            d={'name':element['result']['name'],'type':element['result']['@type'],
                'description':element['result']['description']}

    return d
        #entities_text(element['result']['name'])

query = sys.argv
query=' '.join(query[1:])
try:
    d=entities_text(query)
except KeyError('itemListElement'):
    d=knowledge_graph_entries(query)
with open('output.json','w+') as f:
    json.dump(d,f)
