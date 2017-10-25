from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
import time
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
#import logstash
#import logging
#from .event import Event
import json
from random import uniform
import sys
import urllib3
from http.client import IncompleteRead
import geocoder

reload(sys)
sys.setdefaultencoding('utf8')


AWS_ACCESS_KEY = 'X'
AWS_SECRET_KEY = 'X'
region = 'us-east-2' # For example, us-east-1
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'X' # For example, my-test-domain.us-east-1.es.amazonaws.com


#ElasticSearch object
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    timeout = 10
)

#Twitter credentials:
#Variables that contains the user credentials to access Twitter API

access_token = 'X'
access_token_secret = 'X'
consumer_key = 'X'
consumer_secret = 'XYXZ'
search = ''

# Topic List to be populated in the Dropdown menu
topic = ['Trump', 'Hiliary', 'iOS', 'Android', 'Apple', 'Google', 'Modi', 'NYC','USA']

# Setting the value of Twitter data_dict ti false.
# Note here 'false' is for JavaScript Boolean variable, used in if construct
def esTweets(searchText):

    print 'I am searching for {0}' .format(searchText)
    #print("I am searching for %s" %(searchText))

    res = es.search(index="tweets_coord", doc_type="tweet",  body={"query": {"match": {"text": searchText}}}, size = 100)

    tweets = list()

    #print (res['hits']['hits'])

    for x in res['hits']['hits']:
        tweets.append(x['_source'])
    #print (tweets)

    #searchjson = json.dumps(tweets)
    #tweetDict = dict()

    if (len(tweets) > 0):
        print 'True'
        status = 'true'
    else:
        print 'False'
        status = 'false'

    responseObject = {'status': status, 'tweet':tweets}
    #print(JsonResponse(responseObject).content)
    return JsonResponse(responseObject)

def GoogGeoAPI(address,api=""):
    g = geocoder.google(str(address))

    if(g):
        print 'In GeoCoding True %s' %(address)
        finList = g[0].latlng
        print g[0].latlng
    else:
        print 'In GeoCoding True %s' %(address)
        finList = [None,None]
    return finList

# Method loaded for the first time
def index(request):
    return render(request, 'myapp/mymap.html', {'topics':topic})


# Request sent from the form and used for subsequnet calls
@csrf_protect
def tweetsearch(request):
    if request.method == "POST":

        # Retrieving the value obtained through post request for the dropdown-menu
        search = request.POST.get('search', None)
        print '-x-x-x-x-x-x-x-xx-x-x-x-x-'
        #print (searchText)

    # Testing with the sample data
    class StdOutListener(StreamListener):

        def __init__(self, time_limit=10):
                    self.start_time = time.time()
                    self.limit = time_limit

        def on_data(self, data):

            data_dict = json.loads(data)
            #print(data_dict)
            #Storing the tweets in two different indices:
            #
            # One for the ones that have exact coordinate information
            if (time.time() - self.start_time) < self.limit:
                print 'Here is a new tweet!'

                if 'user' in data_dict.keys():

                    if data_dict['coordinates']:

                        try:
                            longitude, latitude = data_dict['coordinates']['coordinates']
                            #print ' having coordinates {0} {1}' %format(longitude,latitude)
                        except:
                            longitude = None
                            latitude = None

                        doc = {
                             'text': data_dict['text'],
                             'handle': data_dict['user']['screen_name'],
                             'id': data_dict['id'],
                             'longitude': longitude,
                             'latitude': latitude
                             }

                        res = es.index(index="tweets_coord", doc_type='tweet', body=doc)
                        #print(doc['text'])
                        print res['created']


                    elif data_dict['user']['location']:

                        location = GoogGeoAPI(data_dict['user']['location'])

                        #print '-> ->having coordinates %f %f %s' %(location[0], location[1], data_dict['user']['location'])

                        doc = {
                            'text': data_dict['text'],
                            'handle': data_dict['user']['screen_name'],
                            'id': data_dict['id'],
                            'latitude': location[0],
                            'longitude': location[1],

                            }
                        res = es.index(index="tweets_coord", doc_type='tweet', body=doc)
                        #print(doc['text'])
                        print res['created']
                    object = esTweets(search)


                    return True
            else:
                object = esTweets(search)
                print "Else"
                return False


        def on_error(self, status):
            print status
            print 'Damnn'


    #print("It's here")
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track = topic)

    object = esTweets(search)
    return object
