from config import *
from query_db import *
from query_twitter import *
from query_cache import *

def db_insert_all_mentions():
    print "\n -------  Started inserting tweet mentions  -------"
    mentions = []
    tweets = cache_get("Tweets")
    for tweet in tweets:
        print tweet
        mentions.extend(db_insert_tweet_mentions(db_get_tweet(tweet)))

    cache_append("Mentions",mentions)

def db_check_tweet_mentions(tweet_id,user_id):
    query_string = '''MATCH (t:Tweet)-[r:Mention]->(u:User) 
    WHERE u.id_str = {u_id_str} AND
    t.id_str = {t_id_str} RETURN r
    '''
    data = {'u_id_str': user_id, 't_id_str': tweet_id}
    return list(db_query(query_string,data))

def db_insert_tweet_mentions(db_tweet):
    mentions = []
    for id in db_tweet['mentions']:
        print "\t mentions-> "+ id
        if db_check_tweet_mentions(db_tweet['id_str'],id):
            continue
        user = db_get_user(id)
        if not user:   
            user = twitter_get_user_by_id(id)
            db_insert_user(user)
            print "\t New user "+user['id_str']+" fetched and added for tweet mention"   

        query_string = "MATCH (u:User),(t:Tweet) WHERE u.id_str = {u_id_str} AND t.id_str={t_id_str} CREATE (t)-[r:Mention]->(u)"
        data={'u_id_str':user['id_str'], 't_id_str': db_tweet['id_str']}
        mentions.extend(db_tweet['mentions'])
        print "\t Inserted Mention Link"
        db_query(query_string,data)
    return mentions