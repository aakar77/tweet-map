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
import geocoder
#reload(sys)
#sys.setdefaultencoding('UTF8')

#ElasticSearch Credentials
AWS_ACCESS_KEY = 'S'
AWS_SECRET_KEY = 'S'
region = 'us-east-2' # For example, us-east-1
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-mytweetmap-7cquwqe4vjvpdshstcmvyns56' # For example, my-test-domain.us-east-1.es.amazonaws.com

#ElasticSearch object
es = Elasticsearch(
    hosts = [{'host': host, 'port': 445}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

#Twitter credentials:
#Variables that contains the user credentials to access Twitter API
access_token = "s"
access_token_secret = "S"
consumer_key = "S"
consumer_secret = "S"

class StdOutListener(StreamListener):

    def on_data(self, data):

        data_dict = json.loads(data)
        #print(data_dict)
        #Storing the tweets in two different indices:
        #
        # One for the ones that have exact coordinate information
        if 'user' in data_dict.keys():
            if data_dict['coordinates']:
                longitude, latitude = data_dict['coordinates']['coordinates']
                #print longitude,latitude
                doc = {
                     'text': data_dict['text'],
                     'handle': data_dict['user']['screen_name'],
                     'id': data_dict['id'],
                     'longitude': longitude,
                     'latitude': latitude
                }
                res = es.index(index="tweets_coord", doc_type='tweet', body=doc)
                print(res['created'])
                #print data_dict['coordinates']['longitude'], data_dict['coordinates']
                
            #Others that have user's vague location information. Here we validate the location, and index it if it is valid. Otherwise we assign them randomly.
            elif data_dict['user']['location']:
                location = GoogGeoAPI(data_dict['user']['location'])
                #print location[0], location[1]
                if(location[0] != None):
                    doc = {
                        'text': data_dict['text'],
                        'handle': data_dict['user']['screen_name'],
                        'id': data_dict['id'],
                        'longitude': location[0],
                        'latitude': location[1]
                            }
                else:
                    doc = {
                        'text': data_dict['text'],
                        'handle': data_dict['user']['screen_name'],
                        'id': data_dict['id'],
                        'longitude': uniform(-180, 180),
                        'latitude': uniform(-85, 85)
                            }
                res = es.index(index="tweets_loc", doc_type='tweet', body=doc)
                print(res['created'])

        #if 'location' in data_dict.keys()
        #res = es.index(index="tweets", doc_type='tweet', body=doc)
        #i = i+1
        #print(res['created'])
        #with open("Output.txt", "a") as tweet_log:
        #    tweet_log.write(data)
        return True

    def on_error(self, status):
        print (status)
        print ("Damnn")


# Create your views here.

# Topic List to be populated in the Dropdown menu
topic = ['Trump', 'Bieber', 'Apple', 'Korea', 'Kohli', 'Modi', 'NYU', 'iOS', 'Android']

# Setting the value of Twitter data_dict ti false.
# Note here 'false' is for JavaScript Boolean variable, used in if construct
data_dict = 'false'

# Method loaded for the first time
def index(request):
    return render(request, 'myApp/mymap.html', {'topics':topic})

# Request sent from the form and used for subsequnet calls
@csrf_protect
def tweetsearch(request):
    if request.method == "POST":

        # Retrieving the value obtained through post request for the dropdown-menu
        searchText = request.POST.get('search', None)
        print ("%s" % (searchText))

    # Testing with the sample data
    #collectTweets()
    data_dict = gettweets(searchText)
    tweetDict = dict()
    
    ddIndex = topic.index(searchText)
    print(data_dict)
    if (len(data_dict) > 0):
        status = 'true'
    else:
        status = 'false'
    return render(request, 'myApp/mymap.html',{'status': status, 'tweet':data_dict})

#Method for GeoEncoding tweets with no coordinates, but having location information.
def GoogGeoAPI(address,api="AIzaSyAIWnwGb9WRladk_47LmMTH6cte9eC6Ob4"):
  g = geocoder.google(str(address))
  if(g):
      finList = g[0].latlng
  else:
      finList = [None, None]
  return finList
  

def gettweets(search_term):
    res = es.search(q=search_term, size = 20)
    tweets = list()
    #print res
    for x in res['hits']['hits']:
        tweets.append(x['_source'])
    print (tweets)
    return tweets
    
def collectTweets():
    print("It's here")
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.timeOut = 10
    #print(stream)
    stream.sample()

