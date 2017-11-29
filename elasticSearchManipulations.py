from __future__ import print_function

import boto3
import json
import datetime
import time
import sys

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Configuration code for AWS and elastic search
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
region = 'us-east-2' # For example, us-east-1
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-tweetsentiment-qgnbjonsbxhe6v4btn5chvrpgy.us-east-2.es.amazonaws.com'

#ElasticSearch object
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    timeout = 10
)


es.indices.delete(index='tweet_sentiment', ignore=[400, 404])


'''
Debugging
options = {'mappings':
            {
            'tweet':
                {
                'properties': {
                    'text': {'type': 'string'},
                    'handle': {'type': 'string'},
                    'id': {'type': 'string'},
                    'latitude': {'type': 'string'},
                    'longitude': {'type': 'string'},
                    'time' : {'type' : 'date', 'format': 'strict_date_hour_minute_second'}
                    }
                }
            }
        }
# create an index
#es.indices.create(index = 'tweet_sentiment', body = options)

# Properties
body = {'handle': u'mommaFrittsy', 'text': u"RT @TomthunkitsMind: Anthony Weiner is in prison. Bill Clinton was impeached. Bill O'Reilly, Roger Ailes, Harvey Weinstein, Kevin Spacey ",
        'longitude': 29.87476165919128, 'time': str(datetime.datetime.now().replace(microsecond=0).isoformat()), 'latitude': -39.13568497525854, 'id': 935199025485307909 }

res = es.index(index="tweet_sentiment", doc_type='tweet', body=body)
'''
