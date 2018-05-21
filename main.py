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
    #print entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        #print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))

        knowledge_graph_entries(entity.name)

#entities_text(query)

def knowledge_graph_entries(query):

    '''This is using Google Knowledge Graph API'''

    api_key = 'AIzaSyDrQNV9Mb8uS19YHaVM8kNuWgvYu32JlBs'

    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        #'ids':'/m/036hf4',
        'limit': 1,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    for element in response['itemListElement']:
        try:
            print element['result']['name'] + ' (' + str(element['resultScore']) + ')'+' : '+element['result']['detailedDescription']['url']
        except KeyError:
            print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
        if "Person" in element['result']['@type']:
            print "This is a person"
        #entities_text(element['result']['name'])

query = sys.argv
entities_text(' '.join(query[1:]))
