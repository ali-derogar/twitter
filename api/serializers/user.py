def userEntity(item):
    return {
        "id": str(item['_id']),
        "name" : item["name"],
        'email' : item["email"],
        'password' : item["password"],
    }
def usersEntity(entity):
    return [userEntity(item) for item in entity]

# we can use top or bottom for serialize the models , but bottom section work in all models

def serializer_single(a):
    return {**{i : str(a[i]) for i in a if i == "_id"} , **{i : a[i] for i in a if i != "_id"} }
def serializer_group(item):
    return [serializer_single(i) for i in item]
