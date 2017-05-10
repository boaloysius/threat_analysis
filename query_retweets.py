from config import *
from query_cache import *
from query_db import *
from query_os import *
from query_twitter import *

def db_insert_retweets(tweet):
    from_cache = 0
    if 'retweets' not in tweet.keys(): 
        tweet = cache_get_tweet(tweet['id_str'])
        from_cache = 1

    if 'retweets' in tweet.keys():
        if from_cache:
            db_set_retweets_property(tweet['id_str'],tweet['retweets'])

        for retweet_id in tweet['retweets']:
            if db_get_tweet_retweet_relation(tweet['id_str'],retweet_id):
                continue
            
            if not db_get_tweet(retweet_id):
                twitter_get_tweet_by_id(retweet_id)

            db_insert_tweet_retweet_relation(tweet['id_str'],retweet_id)
    else:
        retweets = twitter_get_retweets_by_id(tweet['id_str'])
        if db_set_retweets_property(tweet['id_str'], retweets):
            db_insert_retweets(db_get_tweet(tweet['id_str']))

def db_set_retweets_property(tweet_id,retweets):
    query_string = "MATCH (t:Tweet) WHERE t.id_str = {id_str} SET t.retweets= {retweets} return t"
    data = {"id_str":tweet_id,"retweets":retweets}
    records = db_query(query_string,data)
    records = list(records)
    if not records:
        print "\t Retweets Couldn't be set in Tweet DB"
        return false

    print "\t Retweet property added to Graph"
    return cache_set_retweets(tweet_id, retweets)           

def db_get_tweet_retweet_relation(tweet_id,retweet_id):
    query_string = '''MATCH (t1:Tweet)-[r:Retweet]->(t2:Tweet) 
    WHERE t1.id_str = {t1_id_str} AND
    t2.id_str = {t2_id_str} RETURN r
    '''
    data = {'t1_id_str': tweet_id, 't2_id_str': retweet_id}
    return list(db_query(query_string,data))

def db_insert_tweet_retweet_relation(tweet_id,retweet_id):
    query_string = "MATCH (t1:Tweet),(t2:Tweet) WHERE t1.id_str = {tweet_id} AND t2.id_str={retweet_id} CREATE (t1)-[r:Retweet]->(t2)"
    data={'tweet_id':tweet_id, 'retweet_id': retweet_id}
    db_query(query_string,data)
    print "\t Inserted Link "+tweet_id+" -- Retweet --> "+retweet_id



def db_set_retweet(id_str,retweets):
	query_string = "MATCH (t:Tweet) where t.id_str = {id_str} set t.retweets = {retweets}"
	data = {"id_str":id_str, "retweets": retweets}
	db_query(query_string,data)

def db_insert_all_retweets(tweets=[]):
    print "\n -------  Started inserting tweet retweets  -------"
    if not tweets:
        tweets = cache_get("Tweets")
    for tweet in tweets:
        print tweet
        db_insert_retweets(db_get_tweet(tweet))