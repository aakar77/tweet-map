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

access_token = '2394334112-R1vHGRhhrWvHluIOXDr4HYCIVkmW8LfJjzm1GVM'
access_token_secret = 'bBLF4UE3Y5JN5a0NZHTCcSZmFHPHNUeWiiOrpoJd0gKiU'
consumer_key = '587HSCUOtGCTRKgWTK3NVehs7'
consumer_secret = 'l0vTVXfbAbuJmMYqTJmI9RMGqGdvdQO7yep6xjPcQX5L3AjBri'

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

    data = json.loads(event['Records'][0]['Sns']['Message'])
    topic = topic['topic']

    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        topic = message['topic']
    except Exception as e:
        print('Error in fetching data')
        topic = 'Blockchain'

    '''
    Code for Debugging

    doc = {
        'text': "Aakar",
        'handle': "Hui",
        'id': "12354",
        'latitude': "123",
        'longitude':"234",
        'time' : str(datetime.datetime.now().replace(microsecond=0).isoformat()),
        'topic' : topic
    }

    response = queue.send_message(MessageBody=json.dumps(doc), MessageGroupId='509148512136', MessageDeduplicationId=str(doc['id']))
    '''

    class StdOutListener(StreamListener):

        def __init__(self, time_limit=40):
            self.start_time = time.time()
            self.limit = time_limit
            self.sqs = boto3.resource('sqs')
            self.queue = self.sqs.get_queue_by_name(QueueName='tweetqueue.fifo')
            self.sns = boto3.client('sns',aws_access_key_id='',aws_secret_access_key='',region_name='us-east-2')

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
                                'time' : str(datetime.datetime.now().replace(microsecond=0).isoformat())
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
                                'time' : str(datetime.datetime.now().replace(microsecond=0).isoformat())
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

        # converting the word to search for into list
        topics = topic.split()

        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(track = topics)
    except Exception as e:
        print("Exception occured Twiter Calling",e)
'''
if __name__ == '__main__':
    event = json.dumps({'body' : { 'search' : 'Apple'} }
    mytest = tweet_stream(event,"b")
'''
