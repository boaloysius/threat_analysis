from config import *

class listener (StreamListener):
	def  on_data(self, data):
		try:
			parsed = json.loads(data)
			print parsed['user']['id_str']
			saveFile = open('twitDB.csv','a')
			json.dump(parsed,saveFile)
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException, e:
			print str(e)
			time.sleep(5)

	def on_error(self, status):
		print "error "+str(status)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[-74,40,-73,41])
