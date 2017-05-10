from config import *
from query_db import *

def twitter_get_user_by_id(id_str):        
    try:
        user = api.get_user(id_str)

    except tweepy.TweepError as e:
        print e
        if e[0][0]['code'] == 88:
            time.sleep(60 * 15)
            user = api.get_user(id_str)
        else:         
            print "\t Couldn't fetch User"
        return False

    print "\t Fetched user for "+id_str+", waiting..."
    #time.sleep(5)
    user = user._json
    db_insert_user(user)
    return user

def twitter_get_tweet_by_id(id_str):        
    try:
        tweet = api.get_status(id_str)

    except tweepy.TweepError as e:
        print e
        if e[0][0]['code'] == 88:
            time.sleep(60 * 15)
            user = api.get_status(id_str)
        else:         
            print "\t Couldn't fetch Tweet"
        return False

    print "\t Fetched tweet for "+id_str+", waiting..."
    #time.sleep(5)
    tweet = tweet._json
    db_insert_tweet(tweet)
    return tweet

def twitter_get_retweets_by_id (id_str):
    try:
        retweets = api.retweets(id_str)

    except tweepy.TweepError as e:
        print e
        if e[0][0]['code'] == 88:
            time.sleep(60 * 15)
            retweets = api.retweets(id_str)
        else:         
            print "\t Couldn't fetch User"
        return []

    print "\t Fetched retweets for "+id_str+", waiting..."
    #time.sleep(5)    
    retweet_users = []
    retweet_ids=[]

    for record in retweets:
        tweet = record._json
        retweet_users.append(str(tweet["user"]["id"]))
        db_insert_tweet(tweet)
        os_write_json(tweet, 'retweets/'+str(tweet['id'])+".json",text='Retweet')
        print "--"+ str(tweet['id_str']) +"--"
        retweet_ids.append(str(tweet['id_str']))
    
    cache_append('Retweet_users',retweet_users)

    if not retweet_users:
        print "\t ---- No Retweet found ----"
    else:
        print "\t ---- Retweet found ----"
    
    return retweet_ids
    
def twitter_get_timeline_by_id(id_str):
    try:
        timeline = api.user_timeline(id_str)    

    except tweepy.TweepError as e:
#        if e[0][0]['code'] == 88:
#            time.sleep(60 * 15)
#            timeline = api.user_timeline(id_str)
#        else:         
        print "\t Couldn't fetch User"
        return []

    print "\t Fetched retweets for "+id_str+", waiting..."
    #time.sleep(5) 
    tweets = []
    for tweet in timeline:
        status = tweet._json
        id_str = str(status['id'])
        db_insert_tweet(status)
        tweets.append(id_str)

    return tweets
