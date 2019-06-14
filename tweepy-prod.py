import tweepy
import boto3
import time
import random

access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)



k_client = boto3.client('kinesis')

def getStatus(stream_name):
    try:
        r = k_client.describe_stream(StreamName=stream_name)
        description = r.get('StreamDescription')
        status = description.get('StreamStatus')
        return status
    except k_client.exceptions.ResourceNotFoundException:
        status = 'NOT FOUND'
        return status

def createStream(stream_name):
    try:
        k_client.create_stream(StreamName=stream_name, ShardCount=1)
        print('stream {}'.format(stream_name))
    except k_client.exceptions.ResourceInUseException:
        print('stream %s already in use' %stream_name)
    
    while getStatus().lower()!='active':
        time.sleep(1)
    print('stream %s is active' %sream_name)


if(getStatus('TwitterDemo')!="ACTIVE"):
    createStream('TwitterDemo')
else:
    print('Active Stream')


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener,self).__init__()

    def on_status(self, status):
        if(time.time() - self.start_time)<self.limit:
            record = {}
            record['Data'] = status.text
            record['PartitionKey'] = ''.join(random.choice(['A,B,C']) for _ in range(3))
            k_client.put_records(Records=[record], StreamName='TwitterDemo') #not dynamic as is
            return True
        else:
            return False
    def on_error(self, status):
        print(status)

            


myStreamListener = MyStreamListener(time_limit=20)
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['mufc'])
stream.disconnect()

print('done')