from config import *
import query

user = query.twitter_get_user_by_id(70931004)

saveFile = open('user.csv','a')
json.dump(user,saveFile)
print "Successfully Printed"