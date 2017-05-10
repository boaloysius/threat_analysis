from config import *
from query_db import *
from query_twitter import *
from query_cache import *
from query_db import *

def db_insert_all_timelines():
    print "\n -------  Started inserting user timeline  -------"
    users = []
    users.extend(cache_get("Users"))
    users.extend(cache_get("Mentions"))
    users.extend(cache_get("Retweet_users"))
    for user in users:
        print user
        db_insert_timeline(user)

def db_insert_timeline(user_id):
    user_id = str(user_id)
    user = db_get_user(user_id)
    if not user:
        user = twitter_get_user_by_id(user_id)
    if not user:
        return
    from_cache = 0
    if "timeline" not in user.keys() :
        from_cache = 1
        user = cache_get_user(user['id_str'])
    if "timeline" in user.keys():
        timeline = user['timeline']
        if from_cache :
            db_set_timeline_property(user_id,timeline)
        query_string ="MATCH (t:Tweet) WHERE t.id_str in {timeline} return count(t) as c"
        records = db_query(query_string,{"timeline":timeline})
        record = list(records)
        count = record[0]['c']
        if count == len(timeline):
            print "Timeline Already Exist"
            return
        for tweet_id in timeline:
            if not cache_get_tweet(tweet_id):
                twitter_get_tweet_by_id(tweet_id)
    else:
        timeline = twitter_get_timeline_by_id(user['id_str'])
        cache_append("Timeline",timeline)
        db_set_timeline_property(user['id_str'],timeline)

def db_set_timeline_property(user_id,timeline):
    query_string = "MATCH (u:User) WHERE u.id_str = {id_str} SET u.timeline= {timeline} return u"
    data = {"id_str":user_id,"timeline":timeline}
    records = db_query(query_string,data)
    records = list(records)
    if not records:
        print "\t Timeline Couldn't be set in User DB"
        return false

    print "\t Timeline property added to User Graph"
    return cache_set_timeline(user_id, timeline) 
