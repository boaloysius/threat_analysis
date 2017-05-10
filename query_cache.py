from config import *
from query_os import *

def cache_set_retweets(id_str, retweets):
    file = 'tweets/'+id_str+'.json'
    if os_file_exist(file):
        with open(file,'r') as tweet_file: 
            tweet  = json.load(tweet_file)
        tweet['retweets'] = retweets
        os_write_json(tweet,file," Retweet")
        print "\t Retweets set in Tweet Cache"
        return True
    print "\t Retweets Couldn't be set in Tweet Cache"
    return False

def cache_set_timeline(id_str, timeline):
    file = 'users/'+id_str+'.json'
    if os_file_exist(file):
        with open(file,'r') as user_file: 
            user  = json.load(user_file)
        user['timeline'] = timeline
        os_write_json(user,file," Timeline")
        print "\t Timeline set in User Cache"
        return True
    print "\t Timeline Couldn't be set in User Cache"
    return False

def cache_set(name,data):
    file = 'cache.json'
    with open(file) as cache_file:
        cache = json.load(cache_file)
        cache[name] = data
    os_write_json(cache,file)

def cache_append(name,data):
    file = 'cache.json'
    with open(file) as cache_file:
        cache = json.load(cache_file)
    prior = set(cache[name])
    if not prior.issubset(set(data)):
        cache[name].extend(data)
        os_write_json(cache,file)

def cache_get(name):
    file = 'cache.json'
    with open(file) as cache_file:
        cache = json.load(cache_file)
    return cache[name]