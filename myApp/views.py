from django.shortcuts import render
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


AWS_ACCESS_KEY = 'AKIAJMALUJ4KNADPAUDA'
AWS_SECRET_KEY = 'dEnyd7DOx+b1Xw+f0rCHxlpr44daWmZxZ2Xt+avu'
region = 'us-east-2' # For example, us-east-1
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-tweetmap101-tytzonkx3fobbdw6egsdaem5zy.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com

es = Elasticsearch(
    hosts = [{'host': host, 'port': 445}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)
# Create your views here.

# Topic List to be populated in the Dropdown menu
topic = ['Donald Trump', 'Justin Bieber', 'Apple', 'Taylor Swift', 'Virat Kholi', 'Narendra Modi', 'SRK', 'NYU']

# Setting the value of Twitter data_dict ti false.
# Note here 'false' is for JavaScript Boolean variable, used in if construct
data_dict = 'false'

# Method loaded for the first time
def index(request):
    return render(request, 'myApp/mymap.html', {'topics':topic,'tweet_dict':data_dict})

# Request sent from the form and used for subsequnet calls
def tweetsearch(request):
    if request.method == "POST":

        # Retrieving the value obtained through post request for the dropdown-menu
        searchText = request.POST['dropdown-menu']
        print ("%s" % (searchText))

    # Testing with the sample data
    data_dict = gettweets(searchText)
    ddIndex = topic.index(searchText)
    return render(request, 'myApp/mymap.html',{'tweet_dict':data_dict,'topics':topic, 'search':searchText, 'dropdownIndex':index})



def gettweets(search_term):
    res = es.search(q='the')
    tweets = list()
    #print res
    for x in res['hits']['hits']:
        tweets.append(x['_source'])
    #print tweets
    return tweets
    
    