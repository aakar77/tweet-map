from __future__ import print_function
import json
import time
import boto3

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

def sentiment_analysis(event, context):

    # Choosing the resource from boto3 module
    sqs = boto3.resource('sqs')
    sns = boto3.client('sns',aws_access_key_id='AKIAJX2P4SHIOHCKQGSQ',aws_secret_access_key='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',region_name='us-east-2')
    #sns = boto3.client('sns')
    #topic = sns.Topic('arn:aws:sns:us-east-2:509148512136:tweetSentiment')

    # Configuration for IBM sentiment analysis API
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    username = "",
    password = "",
    version="")

    # Configuration for AWS credentials
    AWS_ACCESS_KEY = ''
    AWS_SECRET_KEY = ''
    region = '' # For example, us-east-1
    service = ''

    try:
        awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)
    except Exception as e:
        print('failure for AWS authentication',e)

    host = 'search-tweetsentiment-qgnbjonsbxhe6v4btn5chvrpgy.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com

    # Configuration for Elasticsearch
    # ElasticSearch object
    es = Elasticsearch(
      hosts = [{'host': host, 'port': 443}],
      http_auth = awsauth,
      use_ssl = True,
      verify_certs = True,
      connection_class = RequestsHttpConnection,
      timeout = 10
    )

    # Get the queue named test
    queue = sqs.get_queue_by_name(QueueName='tweetqueue.fifo')

    time_end = time.time() + 40
    # Process messages by printing out body from test Amazon SQS Queue

    while time.time() < time_end:

        for message in queue.receive_messages(WaitTimeSeconds=10, MaxNumberOfMessages=10):
            try:
                tweet = json.loads(message.body)

                response = natural_language_understanding.analyze(
                    text= tweet['text'],
                    features=Features(sentiment=SentimentOptions()))
                #parsed_data = json.loads(response)

                # Getting the tweet's sentiment and the label(+ve or -ve)
                tweet['sentiment'] = response['sentiment']['document']['score']
                tweet['sentiment_label'] = response['sentiment']['document']['label']

            except Exception as e:
                print('Exception occured while parsing tweets: ', e)
            finally:
                message.delete()

            print (tweet)

            # Indexing tweets in ElasticSearch
            try:
                res = es.index(index="tweet_sentiment", doc_type='tweet', body=json.dumps(tweet))
            except Exception as e:
                print('Exception occured while indexing tweet to ES')

            '''
            # Try except block for publishing the topic
            try:
                # Publish the new tweet to the SNS topic
                sns.publish(
                    TargetArn ='arn:aws:sns:us-east-2:509148512136:tweetSentiment',
                    Message=json.dumps({'default': json.dumps(tweet)}),
                    MessageStructure = 'json'
                )

                print(json.dumps(tweet, indent=2))

            except Exception as e:
                    print('Exception occured while publishing the tweet: {0}'.format(e))
                    break
            '''
    return

if __name__ == '__main__':

    event = {'event':'mouse-click'}
    context = "aakr"
    sentiment_analysis(event, context)
