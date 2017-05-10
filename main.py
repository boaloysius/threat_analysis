from config import *
from query import *

db_insert_users(file="data/twitDB.json")
db_insert_tweets(file="data/twitDB.json")
db_insert_all_mentions()
db_insert_all_retweets()
db_insert_all_timelines()

#db_insert_all_retweets(cache_get("Timeline"))