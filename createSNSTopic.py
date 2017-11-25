import boto3

sns_client = boto3.client('sns')

def topicCreate():
  
  #Creating topic
  topic = sns_client.create_topic(Name='tweetSentiment')
  return topic  

if __name__ == '__main__':
  # Creating a topic
  topic = topicCreate()

