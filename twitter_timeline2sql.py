import sys
import tweepy
import webbrowser
import sqlite3 as lite
import os

# Query terms

Q = sys.argv[1:]

#The d-base file of choice
sqlite3file='tweepytest.db'

#Grabbing auth values stored in environment variables (for security)
CONSUMERKEY = os.environ['CONSUMERKEY']
CONSUMERSECRET = os.environ['CONSUMERSECRET']
ACCESSTOKEN = os.environ['ACCESSTOKEN']
ACCESSTOKENSECRET = os.environ['ACCESSSECRET']

#Tweepy authorization into Twitter API
auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
auth.set_access_token(ACCESSTOKEN, ACCESSTOKENSECRET)
api = tweepy.API(auth)

print("Successful auth for:", api.me().name) #print name of account if auth successful

con = lite.connect(sqlite3file)
cur = con.cursor()
#Uncomment to create new d-base
#cur.execute("CREATE TABLE TWEETS(txt text, author text, created int, source text)")

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        try:
            print("%s\t%s\t%s\t%s\t%s" % (status.text, 
                                      status.author.screen_name, 
                                      status.created_at, 
                                      status.source,
                                      status.id))

            cur.execute("INSERT INTO TWEETS VALUES(?, ?, ?, ?, ?)", (status.text, 
                                                            status.author.screen_name, 
                                                            status.created_at, 
                                                            status.source,
                                                            status.id))
            con.commit()

        except Exception as e:
            print('Encountered Expception:', e, file=sys.stderr)
            pass

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code, file=sys.stderr)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...', file=sys.stderr)
        return True # Don't kill the stream



l = StreamListener()
streamer = tweepy.Stream(auth=auth, listener=l)
print('Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),), file=sys.stderr)

#Sets up userstream
streamer.userstream(_with='followings', async=False) #async=True = failure





