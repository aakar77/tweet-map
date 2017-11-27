from __future__ import print_function

import boto3
import json
import datetime
import time
import sys

def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))

    current_time = datetime.datetime.now().time()

    key1 = "not present"

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
        "body": json.dumps(body)
    }

    return response

if __name__ == '__main__':
  event = {'body' : { 'status' : 'Modi'} }
  mytest = lambda_handler(event,"b")
'''
