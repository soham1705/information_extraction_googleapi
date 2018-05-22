import json
import urllib
import sys

api_key = 'AIzaSyDrQNV9Mb8uS19YHaVM8kNuWgvYu32JlBs'

query = sys.argv
query=' '.join(query[1:])

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
'''for element in response['itemListElement']:
    try:
        print element['result']['name'] + ' (' + str(element['resultScore']) + ')'+' : '+element['result']['detailedDescription']['url']
    except KeyError:
        print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
'''

    #entities_text(element['result']['name'])
