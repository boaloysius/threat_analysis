def create_a_follow_b(node_id,friend_id):
    query_string = "MATCH (a:User),(b:User) WHERE a.id_str = {a_id_str} AND b.id_str = {b_id_str} CREATE (a)-[r:FRIEND]->(b)"
    data = {"a_id_str":node_id, "b_id_str":friend_id}
    db_query(query_string,data)
    session.run(query_string,**data)
    print "Friends Created"