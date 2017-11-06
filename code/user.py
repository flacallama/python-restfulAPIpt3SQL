import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):  # id is a python keyword
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):  #cls was 'self before we went to classmethod'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  #the weird parenthesesis/comma make arg a tupple
        row = result.fetchone() #returns first row if there is one
        if row:  #if there is one row
            # user = User(row[0], row[1], row[2]) - we'd use this if not an @classmethod
            # user = cls(row[0], row[1], row[2])  - this is a good option, but lets clean it up
            user = cls(*row)  #the most clean
        else:
            user = None

        connection.close()
        return user


    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True, #all requests must have prices
        help="this field cannot be left blank"
    )
    parser.add_argument('password',
        type=str,
        required=True, #all requests must have prices
        help="this field cannot be left blank"
    )



    def post(self):

        data = UserRegister.parser.parse_args()

        # CHECK IF USER ALREADY EXISTS - must be before the rest of route
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
