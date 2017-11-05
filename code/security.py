from user import User



# THIS IS HOW WE'D DO IT WITHOUT A USER CLASS
# users = [
#     {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# ]
#
# username_mapping = {'bob': {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }
#
# userid_mapping = { 1: {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }



# BUT NOW WE HAVE A USER CLASS. HERE WE GO:
users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)  # if there isnt a user return None
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)






# we set the mapping up tp find a user by either name or id easily
