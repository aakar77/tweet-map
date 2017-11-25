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

# Topic List to be populated in the Dropdown menu
topic = ['Trump', 'Hiliary', 'iOS', 'Android', 'Apple', 'Google', 'Modi', 'Chicago','Yankees']


def tweet_stream(event, context):

  def GoogGeoAPI(address,api=""):
    g = geocoder.google(str(address))
    if(g):
        finList = g[0].latlng
    else:
        finList = [None, None]
    return finList

  print("Received event: " + json.dumps(event, indent=2))

  current_time = datetime.datetime.now().time()

  class StdOutListener(StreamListener):

    def __init__(self, time_limit=40):
      self.start_time = time.time()
      self.limit = time_limit
      self.sqs = boto3.resource('sqs')
      self.queue = self.sqs.get_queue_by_name(QueueName='tweetqueue.fifo')  

    def on_data(self, data):
      data_dict = json.loads(data)

      if (time.time() - self.start_time) < self.limit:
        print ('Here is a new tweet!')
  
        try:

          if 'user' in data_dict.keys():
            if data_dict['coordinates']:
              longitude, latitude = data_dict['coordinates']['coordinates']

              try:
                doc = {
                  'text': data_dict['text'],
                  'handle': data_dict['user']['screen_name'],
                  'id': data_dict['id'],
                  'longitude': longitude,
                  'latitude': latitude,
                  'time' : str(datetime.datetime.now().time())
                   }
                   
                response = self.queue.send_message(MessageBody=json.dumps(doc), MessageGroupId='509148512136', MessageDeduplicationId=str(data_dict['id']))
                
                print(response)
              except Exception:
                print("Error - 1 Parsing error OR Queuing error")
                
            elif data_dict['user']['location']:
	            location = GoogGeoAPI(data_dict['user']['location'])
	            try:
	              doc = {'text': data_dict['text'],'handle': data_dict['user']['screen_name'],'id': data_dict['id'],'longitude': location[0], 'latitude': location[1], 'time' : str(datetime.datetime.now().time())}
	              response = self.queue.send_message(MessageBody=json.dumps(doc), MessageGroupId='509148512136', MessageDeduplicationId=str(data_dict['id'])) 
	              print(response)
	            except Exception:
	              print("Error - 2 Parsing error OR Queuing error")
	              
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
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track = topic)    
  except Exception:
    print("Exception occured Twiter Calling")


if __name__ == '__main__':
  event = {'body' : { 'status' : 'Modi'} } 
  mytest = tweet_stream(event,"b")

