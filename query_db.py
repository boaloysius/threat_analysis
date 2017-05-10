from config import *
from query_twitter import *
from query_os import *
from query_cache import *

def db_query(query_string, data={}):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth= basic_auth("neo4j","hexagon"))
    session = driver.session()
    #adding a unique constraint; this ensures that same Person is not added twice
    query_return = session.run(query_string,**data)
    session.close()
    return query_return

def db_insert_user(user):

    user['id_str'] = str(user['id'])

    query_string = """
        MERGE (u:User {id_str:{id_str}}) 
        ON CREATE SET
        u.name={name},
        u.screen_name={screen_name},
        u.description={description},
        u.url={url},
        u.followers_count={followers_count},
        u.friends_count={friends_count},
        u.listed_count={listed_count},
        u.statuses_count={statuses_count},
        u.favourites_count={favourites_count},
        u.location={location},
        u.time_zone={time_zone},
        u.utc_offset={utc_offset},
        u.lang={lang},
        u.profile_image_url={profile_image_url},
        u.geo_enabled={geo_enabled},
        u.verified={verified},
        u.notifications={notifications},
        u.is_set= true
        ON MATCH SET
        u.is_set = 0 RETURN u.is_set as is_set
    """

    records = db_query(query_string, user)
    records = list(records)
    is_set = records[0]['is_set']
    if is_set:
        filename = 'users/'+user['id_str']+'.json'
        if not os_file_exist(filename):
            os_write_json(user, filename, "User")
            return
        print "\t Inserted User "+user['id_str']+" to Database"
    else:
        print "\t User Match DB"

def db_insert_users(file):
    print "\n -------  Started inserting users  -------"    
    i = open(file,'rb')
    user_ids = []
    for tweet in i:
        parsed = json.loads(tweet)
        print str(parsed['user']['id_str'])
        db_insert_user(parsed['user'])
        user_ids.append(parsed['user']['id_str'])
    cache_append("Users",user_ids)

def db_insert_tweet(tweet):

    tweet['id_str'] = str(tweet['id'])

    query_string = """
        MERGE (t:Tweet {id_str:{id_str}})  
        ON CREATE SET 
        t.id_str = {id_str},
        t.text={text},
        t.in_reply_to_user_id_str={in_reply_to_user_id},
        t.retweeted={retweeted},
        t.created_at={created_at}
    """
    keys = tweet.keys()

    mentions = []
    if tweet["entities"]["user_mentions"]:
        for mention in tweet["entities"]["user_mentions"]:
            mentions.append(mention["id_str"])
    
    tweet["mentions"] = mentions    
    query_string = query_string + ", t.mentions = {mentions}"    

    if "retweets" in keys:
        query_string = query_string + ", t.retweets = {retweets}"
    if "timeline" in keys:
        query_string = query_string + ", t.timeline = {timeline}"

    if "timestamp_ms" in keys:
        query_string = query_string + ", t.timestamp_ms = {timestamp_ms}"    
    if "is_quote_status" in keys:
        query_string = query_string + ", t.is_quote_status = {is_quote_status}"
    if "quoted_status_id" in keys:
        query_string = query_string + ", t.quoted_status_id = {quoted_status_id}"
    if "possibly_sensitive" in keys:
        query_string = query_string + ", t.possibly_sensitive = {possibly_sensitive}"
    query_string = query_string+",t.is_set=1 ON MATCH SET t.is_set = 0 RETURN t.is_set as is_set"

    records = db_query(query_string, tweet)
    records = list(records)
    is_set = records[0]['is_set']
    if is_set:    
        db_create_author_tweet_relation(tweet)
        filename = 'tweets/'+tweet['id_str']+'.json'    
        if not os_file_exist(filename):
            os_write_json(tweet, filename," Tweet")
        print "\tInserted Tweet "+tweet['id_str']+ " to Database"         
    else:
        print "\t Tweet MATCH DB"

def db_insert_tweets(file):
    print "\n -------  Started inserting tweets -------"    
    i = open(file,'rb')
    tweet_ids=[]
    for tweet in i:
        tweet = json.loads(tweet)
        print str(tweet['id'])
        db_insert_tweet(tweet)
        
        tweet_ids.append(tweet['id_str'])
    cache_append("Tweets",tweet_ids)

def db_create_author_tweet_relation(tweet):
    print "\t Author -> " + tweet['user']['id_str']
    if db_author_tweet_relation(tweet['id_str'],tweet['user']['id_str']):
        return
    db_insert_user(tweet['user'])
    query_string = "MATCH (u:User),(t:Tweet) WHERE u.id_str = {u_id_str} AND t.id_str={t_id_str} CREATE (u)-[r:Tweeted]->(t)"
    data={'u_id_str':tweet['user']['id_str'], 't_id_str': tweet['id_str']}
    print "\t Inserted Author Tweet Link"
    db_query(query_string,data)

def db_get_user(id_str):
    query_string = "Match (u:User) WHERE u.id_str={id_str} RETURN u"
    data={'id_str':id_str} 
    records = db_query(query_string,data)
    records = list(records)
    if records:
        return records[0]["u"].properties
    user = cache_get_user(id_str)
    return user

def db_get_tweet(id_str):
    query_string = "Match (t:Tweet) WHERE t.id_str={id_str} RETURN t"
    data={'id_str':id_str} 
    records = db_query(query_string,data)
    records = list(records)
    if records:
        return records[0]['t'].properties
    tweet = cache_get_tweet(id_str)
    return tweet


def db_author_tweet_relation(tweet_id,user_id):
    query_string = '''MATCH (u:User)-[r:Tweeted]->(t:Tweet) 
    WHERE u.id_str = {u_id_str} AND
    t.id_str = {t_id_str} RETURN r
    '''
    data = {'u_id_str': user_id, 't_id_str': tweet_id}
    return list(db_query(query_string,data))


def db_get_all_users():
    query_string = "MATCH (u:User) RETURN u"
    records = db_query(query_string)
    users=[]
    for record in records:
    	users.append(record['u'].properties)
    return users

def db_get_all_tweets():
    query_string = "MATCH (t:Tweet) RETURN t"
    records = db_query(query_string)
    tweets=[]
    for record in records:
        tweets.append(record['t'].properties)
    return tweets


############################################################################################

def cache_get_retweets(id_str):
    file = 'tweets/'+id_str+'.json'
    if os_file_exist(file):
        with open(file) as tweet:
            tweet = json.load(tweet_file)
        if 'retweets' in tweet.keys():
            db_set_retweet(id_str,cache_tweet['retweets'])
            return tweet['retweets']
    return False

def cache_get_user(id_str):
    file = 'users/'+id_str+'.json'
    if os_file_exist(file): 
        print "\t User Found in Cache"
        with open(file) as user_file:
            user = json.load(user_file)
        db_insert_user(user)
        return user
    return False

def cache_get_tweet(id_str):
    file = 'tweets/'+id_str+'.json'
    
    if os_file_exist(file): 
        print "\t Tweet Found in Tweet Cache"
        with open(file) as tweet_file:
            tweet = json.load(tweet_file)
        db_insert_tweet(tweet)
        return tweet
    
    return False
