from __future__ import print_function
import json
import time
import boto3

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions


def sentiment_analysis(event, context):
    
  # Choosing the resource from boto3 module
  sqs = boto3.resource('sqs')

  natural_language_understanding = NaturalLanguageUnderstandingV1(
  username = "X",
  password = "X",
  version="2017-02-27")


  # Get the queue named test
  queue = sqs.get_queue_by_name(QueueName='tweetqueue.fifo')
  time_end = time.time() + 40
  

  # Process messages by printing out body from test Amazon SQS Queue
  while time.time() < time_end :
    for message in queue.receive_messages(WaitTimeSeconds=10, MaxNumberOfMessages=10):
      try:

        tweet = json.loads(message.body)

        response = natural_language_understanding.analyze(
          text= tweet['text'],
          features=Features(sentiment=SentimentOptions()))
        
        tweet['sentiment'] = response['sentiment']['document']['score'] 
        #parsed_data = json.loads(response)
        
        tweet['sentiment_label'] = response['sentiment']['document']['label']
          
        print(json.dumps(tweet, indent=2))
      
      except Exception:
        print('Exception occured')
      finally:
        message.delete()
  return             

if __name__ == '__main__':
  
  event = {'event':'mouse-click'}
  context = "aakr"
  sentiment_analysis(event, context)


