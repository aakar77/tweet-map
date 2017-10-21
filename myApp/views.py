from django.shortcuts import render
import json
import time

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
    data_dict = {"tweet": [
                    { "lat": 40.712772, "long": -73.968285, "tweetData": "Hello"},
                    { "lat": 28.018349 , "long": -82.764473, "tweetData": "DOnald" },
                    { "lat": 34.426388, "long": -117.300880, "tweetData": "Virginia" }
                ]}

    return render(request, 'myApp/mymap.html',{'tweet_dict':data_dict,'topics':topic, 'search':searchText})
