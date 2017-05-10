from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import json
import time 
from neo4j.v1 import GraphDatabase, basic_auth
import tweepy
import copy
from pathlib import Path

import sys

class Logger(object):
    def __init__(self):
    	log_file=open("logfile.txt", "w")
    	log_file.write("------------------------ Project Log ------------------------")
    	log_file.close()
        self.terminal = sys.stdout
        self.log = open("logfile.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()

#authenticaing twitter api user

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

#get neo4j set up
#note, you have to have neo4j running and on the default port
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "hexagon"))
try:
	session = driver.session()
	#adding a unique constraint; this ensures that same User is not added twice
	session.run("CREATE CONSTRAINT ON (a:User) ASSERT a.id_str IS UNIQUE")
	session.close()
except:
    pass

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)