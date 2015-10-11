import sys
import tweepy
import webbrowser
import sqlite3 as lite
import os

# Query terms

Q = sys.argv[1:]

sqlite3file='/home/pi/junk_code/tweepy.db'

CONSUMERKEY = os.environ["CONSUMERKEY"]
CONSUMERSECRET = os.environ['CONSUMERSECRET']
ACCESSTOKEN = os.environ['ACCESSTOKEN']
ACCESSTOKENSECRET = os.environ['ACCESSSECRET']

auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
auth.set_access_token(ACCESSTOKEN, ACCESSTOKENSECRET)
api = tweepy.API(auth)

print("Successful auth for:", api.me().name) #print name of account if auth successful

con = lite.connect(sqlite3file)
cur = con.cursor()
cur.execute("CREATE TABLE TWEETS(txt text, author text, created int, source text)")

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        try:
            print("%s\t%s\t%s\t%s" % (status.text, 
                                      status.author.screen_name, 
                                      status.created_at, 
                                      status.source,))

            cur.execute("INSERT INTO TWEETS VALUES(?, ?, ?, ?)", (status.text, 
                                                            status.author.screen_name, 
                                                            status.created_at, 
                                                            status.source))
            con.commit()

        except Exception as e:
            #print(>> sys.stderr, 'Encountered Exception:', e)
            print('Encountered Expception:', e, file=sys.stderr)
            pass

    def on_error(self, status_code):
        #print(>> sys.stderr, 'Encountered error with status code:', status_code)
        print('Encountered error with status code:', status_code, file=sys.stderr)
        return True # Don't kill the stream

    def on_timeout(self):
        #print(>> sys.stderr, 'Timeout...')
        print('Timeout...', file=sys.stderr)
        return True # Don't kill the stream

#streaming_api = tweepy.streaming.Stream(auth, MyStreamListener(), timeout=60)

l = StreamListener()
streamer = tweepy.Stream(auth=auth, listener=l)
streamer.userstream(_with='followings', async=False)





#myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth = api.auth, listener())

#print(>> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),))
print('Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),), file=sys.stderr)

#myStream.userstream("with=following")
