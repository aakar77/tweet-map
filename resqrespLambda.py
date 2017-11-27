from __future__ import print_function

import boto3
import json
import datetime
import time
import sys

def stringParsing(myString):

    whitelist = set('abcdefghijklmnopqrstuvwxy  :ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    key = ''.join(filter(whitelist.__contains__, myString))
    return(key[9:])

def request_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))

    key = "not present"

    if event['body'] is not None:
        #data = event['body']
        key = stringParsing(event['body'])
        print(key)

    # For data[6:] "atus' : 'Trump'\n}" is response

    ## Code for fectching the user keyword from the request
    # Extract from event['body']

    ## Code for Triggering TweetStream Lambda


    ## Code for fetching data from ElasticSearch

    # We can compare for latest tweets from the timer associated with the tweet


    ## Code for sending back the response to User

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : 'https://s3.us-east-2.amazonaws.com'
        },
        "body": json.dumps(key)
    }

    return response

'''
if __name__ == '__main__':
  event = {'body' : "{ 'status' : 'Modi'}" }
  #event = "{/\n status : Trump }"
  mytest = request_handler(event,"b")
'''
