from flask import Flask, jsonify, Blueprint, request
from flask_restful import Resource, Api, reqparse, abort
import json
import datetime

class lookuser(Resource):
    def get(self):
        with open('user.txt') as json_file:  
            data = json.load(json_file)
            return data

class looktweet(Resource):
    def get(self):
        with open('tweet.txt') as json_file:  
            data = json.load(json_file)
            return data

class login(Resource):
    def post(self):
        with open('user.txt') as json_file:  
            data = json.load(json_file)
        email = request.json["email"]
        password = request.json["password"]
        for user in data:
            if user["email"] == email and user["password"] == password:
                return user,200
            elif user["email"] != email and user["password"] == password:
                return "Wrong Email",400
            elif user["email"] == email and user["password"] != password:
                return "Wrong Password",400
            else:
                return "Please Sign Up",400

def registeredEmail(name):
    with open('user.txt') as json_file:  
            data = json.load(json_file)
    for user in data:
        if user["email"] == name:
            abort(400, message = "Email Already Registered")

def registeredUsername(name):
    with open('user.txt') as json_file:  
            data = json.load(json_file)
    for user in data:
        if user["username"] == name:
            abort(400, message = "Username Not Available")

class signup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "Email Required",
            required = True,
            location =["json"]
        )
        self.reqparse.add_argument(
            "password",
            help = "Password Required",
            required = True,
            location =["json"]
        )
        self.reqparse.add_argument(
            "username",
            help = "Username Required",
            required = True,
            location =["json"]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        registeredEmail(request.json["email"])
        registeredUsername(request.json["username"])
        user.append(request.json)
        with open('user.txt', 'w') as outfile:  
            json.dump(user, outfile)
        return "Account Successfully Made",200

class tweeting(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "Email Required",
            required = True,
            location =["json"]
        )
        self.reqparse.add_argument(
            "tweet",
            help = "Tweet Required",
            required = True,
            location =["json"]
        )
        super().__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        with open('tweet.txt') as json_file:  
            tweet = json.load(json_file)
        tweeps = request.json
        time = str(datetime.datetime.now())
        tmp = {}
        tmp["datetime"] = time
        req = tweeps.copy()
        req.update(tmp)
        tweet.append(req)
        with open('tweet.txt', 'w') as outfile:  
            json.dump(tweet, outfile)
        return "Tweeted",200

class editTweet(Resource):
    def put(self):
        email = request.json["email"]
        oldTwit = request.json["old tweet"]
        newTwit = request.json["new tweet"]
        with open('tweet.txt') as json_file:  
            tweet = json.load(json_file)
        for index in range(len(tweet)):
            if tweet[index]['email'] == email and tweet[index]['tweet'] == oldTwit:
                tweet[index]['tweet'] = newTwit
                tweet[index]['time'] = str(datetime.datetime.now())
                with open('tweet.txt', 'w') as outfile:  
                    json.dump(tweet, outfile)
                    outfile.close()
                return "tweet telah diubah", 201
            return "tweet tidak ada", 400

class delete(Resource):
    def delete(self):
        with open('tweet.txt') as json_file:  
            data = json.load(json_file)
        for user in data:
            if user["email"] == request.json['email'] and user["tweet"] == request.json['tweet']:
                data.remove(user)
                with open('tweet.txt', 'w') as outfile:
                    outfile.write(json.dumps(data))
                    outfile.close()
                return "DELETED",200
        return "ERROR",400

tweeps_api = Blueprint('resources/tweeps', __name__)
api = Api(tweeps_api)
api.add_resource(lookuser, 'user')
api.add_resource(looktweet,'tweet')
api.add_resource(login,'login')
api.add_resource(signup,'signup')
api.add_resource(tweeting,'tweeting')
api.add_resource(editTweet, 'tweetedit')
api.add_resource(delete,'delete')