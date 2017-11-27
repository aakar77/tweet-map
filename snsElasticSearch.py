from __future__ import print_function

import json
import time
import boto3

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def sns_elastic_handler(event, context):

  AWS_ACCESS_KEY = 'X'
  AWS_SECRET_KEY = 'X'
  region = 'us-east-2' # For example, us-east-1
  service = 'es'

  awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

  host = 'search-tweetsentiment-qgnbjonsbxhe6v4btn5chvrpgy.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-    east-1.es.amazonaws.com

  #ElasticSearch object
  es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    timeout = 10
  )

  message = event['Records'][0]['Sns']['Message']

  res = es.index(index="tweet_sentiment", doc_type='tweet', body=message)
  print (res)

'''
if '__name__' == '__main__':

  event = {'aakar' : 'mykar'}
  sns_elastic_handler(event, 'sakar')
'''
