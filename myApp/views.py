from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
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
import sys


AWS_ACCESS_KEY = 'AKIAIHKXJ52GYTQRYZPQ'
AWS_SECRET_KEY = 'lxiD3GZ6CidOCXEfePFEJXG2KXudScOjUCOKQ3oW'
region = 'us-east-2' # For example, us-east-1
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-mytweetmap-7cquwqe4vjvpdshstcmvyns56y.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com

es = Elasticsearch(
    hosts = [{'host': host, 'port': 445}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

class StdOutListener(StreamListener):

    def on_data(self, data):

        data_dict = json.loads(data)
        if 'user' in data_dict.keys():
            if data_dict['coordinates']:
                longitude, latitude = data_dict['coordinates']['coordinates']
                print longitude,latitude
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
            elif data_dict['user']['location']:
                location = GoogGeoAPI(data_dict['user']['location'])
                print location[0], location[1]
                if(location[0] != None):
                    doc = {
                        'text': data_dict['text'],
                        'handle': data_dict['user']['screen_name'],
                        'id': data_dict['id'],
                        'longitude': location[0],
                        'latitude': location[1]
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
        print "Damnn"


# Create your views here.

# Topic List to be populated in the Dropdown menu
topic = ['Donald Trump', 'Justin Bieber', 'Apple', 'Taylor Swift', 'Virat Kholi', 'Narendra Modi', 'SRK', 'NYU', 'the']

# Setting the value of Twitter data_dict ti false.
# Note here 'false' is for JavaScript Boolean variable, used in if construct
data_dict = 'false'

# Method loaded for the first time
def index(request):
    return render(request, 'myApp/mymap.html', {'topics':topic,'tweet_dict':data_dict, 'dropdownIndex':ddIndex})

# Request sent from the form and used for subsequnet calls
def tweetsearch(request):
    if request.method == "POST":

        # Retrieving the value obtained through post request for the dropdown-menu
        searchText = request.POST['dropdown-menu']
        print ("%s" % (searchText))

    # Testing with the sample data
    collectTweets()
    data_dict = gettweets(searchText)
    ddIndex = topic.index(searchText)
    print(data_dict)
    return render(request, 'myApp/mymap.html',{'tweet_dict':data_dict,'topics':topic, 'search':searchText, 'dropdownIndex':ddIndex})

#Method for GeoEncoding tweets with no coordinates, but having location information.
def GoogGeoAPI(address,api="AIzaSyAIWnwGb9WRladk_47LmMTH6cte9eC6Ob4"):
  base = r"https://maps.googleapis.com/maps/api/geocode/json?"
  addP = "address=" + address.replace(" ","+")
  GeoUrl = base + addP.encode('utf-8') + "&key=" + api
  response = urllib.urlopen(GeoUrl)
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  if jsonData['status'] == 'OK':
    resu = jsonData['results'][0]
    finList = [resu['geometry']['location']['lat'],resu['geometry']['location']['lng']]
  else:
    finList = [None,None]
  #time.sleep(delay) #in seconds
  return finList
  

def gettweets(search_term):
    res = es.search(q=search_term)
    tweets = list()
    #print res
    for x in res['hits']['hits']:
        tweets.append(x['_source'])
    print (tweets)
    return tweets
    
def collectTweets():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.sample()

