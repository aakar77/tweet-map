from __future__ import print_function
import json
import time
import boto3

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

def sentiment_analysis(event, context):

    # Choosing the resource from boto3 module
    sqs = boto3.resource('sqs')

    sns = boto3.client('sns',aws_access_key_id='',aws_secret_access_key='',region_name='')
    #sns = boto3.client('sns')
    #topic = sns.Topic('arn:aws:sns:us-east-2:509148512136:tweetSentiment')

    natural_language_understanding = NaturalLanguageUnderstandingV1(
    username = "ec235ab4-4a96-4c36-a6ab-b4bbcadd60d9",
    password = "4XeXGzrmxnBQ",
    version="2017-02-27")

    # Get the queue named test
    queue = sqs.get_queue_by_name(QueueName='tweetqueue.fifo')

    time_end = time.time() + 30
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

            except Exception:
                print('Exception occured')
            finally:
                message.delete()
    return


if __name__ == '__main__':

    event = {'event':'mouse-click'}
    context = "aakr"
    sentiment_analysis(event, context)
