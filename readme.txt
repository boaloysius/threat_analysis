:config initialNodeDisplay: 3000
{"Retweet_users”:[],”Users”:[],”Tweets”:[],”Mentions”:[],”Timeline”:[]}

"MATCH p=(u1:User)-[:Tweeted]->(:Tweet)-[:Retweet]->(:Tweet)<-[:Tweeted]-(u2:User) RETURN u1.id_str AS u1,u2.id_str AS u2"

"MATCH p=(u1:User)-[:Tweeted]->(:Tweet)-[:Mention]->(u2:User) RETURN u1.id_str AS u1,u2.id_str AS u2"