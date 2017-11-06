from werkzeug.security import safe_str_cmp  # compare 2 strings across all platforms
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



# # BUT NOW WE HAVE A USER CLASS. HERE WE GO:
# users = [
#     User(1, 'bob', 'asdf')
# ]
#
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}
#
# WE WERE USING THIS BEFORE THE DB
# def authenticate(username, password):
#     user = username_mapping.get(username, None)  # if there isnt a user return None
#     if user and user.password == password:
#         return user
#
# def identity(payload):
#     user_id = payload['identity']
#     return userid_mapping.get(user_id, None)
#

# THIS IS THE NEW WAY WITH THE DB
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)


# we set the mapping up tp find a user by either name or id easily
