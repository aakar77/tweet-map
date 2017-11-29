from __future__ import print_function

import boto3
import json
import datetime
import time
import sys

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# returns the parsed string containing the key
def stringParsing(myString):

    whitelist = set('abcdefghijklmnopqrstuvwxy  :ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    key = ''.join(filter(whitelist.__contains__, myString))
    return(key[9:])

#  fetches the data based on the keyword from the server and sends it back to user
def fetchElasticSearch(keyword, es):

    searchQuery = {"query": {"match": {"text": keyword}}}

    try:
        response = es.search(index="tweet_sentiment", doc_type="tweet",  body=searchQuery, size = 100)
    except Exception as e:
        print('Error in fetching tweets',e)

    tweets = list()

    for x in response['hits']['hits']:
        tweets.append(x['_source'])

    if (len(tweets) > 0):
        print ('True')
        status = 'true'
        responseObject = {'status': status, 'tweet':tweets}
    else:
        print ('False')
        status = 'false'
        responseObject = {'status': status}

    return responseObject

def request_handler(event, context):

    # Getting boto3 client
    sns = boto3.client('sns',aws_access_key_id='',aws_secret_access_key='',region_name='us-east-2')
    #sns = boto3.client('sns')

    #print("Received event: " + json.dumps(event, indent=2))

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

    # Fetching the data from the request

    if event['body'] is not None:

        # Parsing the body, event['body'] gives JSON object in the form of "{\n 'status' : 'Trump' }"
        mydata = json.loads(event['body'])
        key = mydata['search']
        #key = mydata['search']

        es.indices.delete(index='tweet_sentiment', ignore=[400, 404])

        # Code for Triggering TweetStream Lambda
        snsObject = {'topic' : key}
        try:
            sns.publish(
                TargetArn ='arn:aws:sns:us-east-2:509148512136:requestNotify',
                Message=json.dumps({'default': json.dumps(snsObject)}),
                MessageStructure = 'json'
            )
        except Exception as e:
            print('Error while SNS', e)

        '''
        # Delay 10 seconds for inclusion of new tweets
        try:
            time.sleep(8)
        except Exception as e:
            print('Error in While sleep', e)
        '''


        ## Code for fetching data from ElasticSearch
        #responseObj = fetchElasticSearch(key,e)
        responseObj = {'status' : 'true'}

    else:
        # Construct an error packet
        responseObj = {'status' : 'false'}

    ## Sending the response back to the user

    response = {
        'statusCode' : 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(responseObj)
    }
    return response

'''
if __name__ == '__main__':
  data = json.dumps( {"search" : "Trump"})
  event = {"body" : data}
  #event = "{search : Trump }"
  mytest = request_handler(event,"b")

  print (mytest)
'''
