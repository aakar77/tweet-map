from django.conf.urls import include, url
from . import views

urlpatterns = [

    #Only empty string will match this
    # name = 'post_list' is the name of the URL used to identify the view
    url(r'^index$', views.index, name='index'),
    url(r'^search$', views.tweetsearch, name='index')
]

# Djago will take everything mentioned here and place it in the variable called pk
# \d also tells us that it can only be a digit, not a letter (so everything between 0 and 9).
# + means that there needs to be one or more digits there. So something like http://127.0.0.1:8000/post//
# is not valid, but
