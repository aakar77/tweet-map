from __future__ import print_function
from random import uniform
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from http.client import IncompleteRead

import boto3
import json
import datetime
import time
import json
import sys
import geocoder
import sys
import urllib3

reload(sys)
sys.setdefaultencoding('utf8')

access_token = 'X'
access_token_secret = 'X'
consumer_key = 'X'
consumer_secret = 'X'

print('Loading function')

def tweet_stream(event, context):

    def GoogGeoAPI(address,api=""):
        g = geocoder.google(str(address))

        if(g):
            finList = g[0].latlng
        else:

            y, x = uniform(-120,120), uniform(-40,70)
            # Generating random co-ordinates
            finList = [x,y]
        return finList

    print("Received event: " + json.dumps(event, indent=2))

    current_time = datetime.datetime.now().time()

    class StdOutListener(StreamListener):

        def __init__(self, time_limit=40):
            self.start_time = time.time()
            self.limit = time_limit
            self.sqs = boto3.resource('sqs')
            self.queue = self.sqs.get_queue_by_name(QueueName='tweetqueue.fifo')
            self.sns = boto3.client('sns',aws_access_key_id='AKIAJX2P4SHIOHCKQGSQ',aws_secret_access_key='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',region_name='us-east-2')

        def on_data(self, data):
            data_dict = json.loads(data)

            if (time.time() - self.start_time) < self.limit:
                print ('Here is a new tweet!')

                try:
                    if 'user' in data_dict.keys():
                        if data_dict['coordinates']:
                            longitude, latitude = data_dict['coordinates']['coordinates']

                            doc = {
                                'text': data_dict['text'],
                                'handle': data_dict['user']['screen_name'],
                                'id': data_dict['id'],
                                'latitude': latitude,
                                'longitude': longitude,
                                'time' : str(datetime.datetime.now().replace(microsecond=0).isoformat()),
                            }
                            print(doc)

                            try:

                                #Adding the data to SQS queue
                                response = self.queue.send_message(MessageBody=json.dumps(doc), MessageGroupId='509148512136', MessageDeduplicationId=str(data_dict['id']))

                            except Exception as e:
                                print('Error While adding to SQS OR Tweet Parsing Error')

                            snsResponse = {'status' : 'OK' }

                            try:
                                    #Triggering SNS for Sentiment Analysis, not sending tweets from here
                                self.sns.publish(
                                    TargetArn ='arn:aws:sns:us-east-2:509148512136:sqsPoll',
                                    Message=json.dumps({'default': json.dumps(snsResponse)}),
                                    MessageStructure = 'json'
                                )
                            except Exception as e:
                                print('Error while SNS - 4 - 1', e)


                        elif data_dict['user']['location']:
                            location = GoogGeoAPI(data_dict['user']['location'])

                            doc = {
                                'text': data_dict['text'],
                                'handle': data_dict['user']['screen_name'],
                                'id': data_dict['id'],
                                'latitude': location[0],
                                'longitude': location[1],
                                'time' : str(datetime.datetime.now().replace(microsecond=0).isoformat()),
                            }
                            print(doc)

                            try:
                                #Adding the data to SQS queue

                                response = self.queue.send_message(MessageBody=json.dumps(doc), MessageGroupId='509148512136', MessageDeduplicationId=str(data_dict['id']))

                            except Exception as e:
                                print('Error While adding to SQS OR Tweet Parsing Error -- Geo 2')

                            snsResponse =  {'status' : 'OK'}

                            try:
                                #Triggering SNS for Sentiment Analysis, not sending tweets from here

                                self.sns.publish(
                                    TargetArn ='arn:aws:sns:us-east-2:509148512136:sqsPoll',
                                    Message=json.dumps({'default': json.dumps(snsResponse)}),
                                    MessageStructure = 'json'
                                )
                            except Exception as e:
                                print('Error while SNS - 4 - 2', e)
                        return True
                    else:
                        return False
                except Exception:
                    print("Error - Incomplete Read")
                    return False
            else:
                return False

        def on_error(self, status):
            print (status)
            print ('Error occured')

    try:

        topic = ['Trump', 'Obama', 'iOS', 'Android', 'Apple', 'Google', 'Modi', 'Chicago','Hacker']
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        message = event['Records'][0]['Sns']['Message']
        topic = message['topic']

        topic = topic.split()

        stream.filter(track = topic)
    except Exception as e:
        print("Exception occured Twiter Calling",e)

'''
if __name__ == '__main__':
    event = {'body' : { 'status' : 'Apple'} }
    mytest = tweet_stream(event,"b")
'''
