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
#consumer_key="3IQSCfwKEpZrzhzbb9tNh97ef"
#consumer_secret="BJTX7AirnX2lx1gYpbMO0kYdpapJ9T2zAtCcpgCjRKSWVkG4Tq"
#access_token="2903480370-rHqJZnGM13R8La3CcURPvfpQQQ1GWActgiucaMD"
#access_token_secret="JZQhhPKnWEhmi9TvfCMvIgoeRR6ZdHFH8itGl2YEtvEen"

#consumer_key="OMSte2W3X7wEtGcPyE00hTsdc"
#consumer_secret="dMumB2l97KwZK9W5CRZEgK4BUxLt9CjgqZnjTUKrhzzBkDbfZw"
#access_token="2903480370-r4PSSsvqrfPnEXrlOiOUs7pXdMjOGR9cmiWCu3p"
#access_token_secret="3ob5CFtAW0UCutYlkxUoo2LnnZiGPhpeqD3qS6cAyOuHp"

consumer_key="ruVYXIGbeDMbZcKXTBbV7GCxv"
consumer_secret="FDq6cfLtYi7hKrd395S4QcPYXDf91Qb8kxK444aXi42Ies4Vau"
access_token="2903480370-L2x4s7UYDdo0oLM5GKRgUdgy6wkKAIIlT97No7R"
access_token_secret="TPCLMmmIK4VuThb3Y7aYq40Jsr2CKhISzE0l4r0XRXrNt"

#consumer_key="40VYKBHqvgvSR5mPO4h1vans4"
#consumer_secret="fEzpxvaIMAiL8UVgK9qH1aIzpeBwgGVf3YsCBysvKn0XRTYNSl"
#access_token="856795636032655360-U4yusdL3qjK3p4UlfPe53XLp6kMPmdc"
#access_token_secret="L82jhIDG2VdxndTmTBaPTdMYfICr5P0jLPST90lm1vM39"

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