from __future__ import print_function

from __future__ import print_function
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="X",
  password="X",
  version="2017-02-27")

response = natural_language_understanding.analyze(
    text='Bruce Banner is the Hulk and Bruce Wayne is BATMAN! Superman fears not Banner but Wayne',
    features=Features(sentiment=SentimentOptions()))

#parsed_data = json.loads(response)
sentiment = response['sentiment']['document']['score']
s_label = response['sentiment']['document']['label']

print (sentiment)
print (s_label)
