import json
import os
from flask import Flask, jsonify, request, redirect, url_for, Response
from redis import StrictRedis
from slackclient import SlackClient
import zmq
import sys
import time

app = Flask(__name__)
redis = StrictRedis(host='redis')

@app.route('/')
def api_live():
    """ root endpoint; serves to notify that the application is live """
    return Response(json.dumps({'message' : 'Api is live.'}), 200)

@app.route('/pub_test')
def pub_test():
    try:
        _publisher.bind(url)
        time.sleep(1)
        _publisher.send_string('hello from flask')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally: _publisher.unbind(url)


    return Response(json.dumps({'message' : 'ZMQ pinged.'}), 200)

@app.route('/get_users')
def get_users():
    users = this_slack_client.api_call("users.list")
    current_users = {user['id']:user['name'] for user in users['members']}
    for user_id, user_name in current_users.items():
        redis.set(user_id, user_name)
    return Response(json.dumps({'message' : 'Got users from slack'}), 200)

@app.route('/read_users')
def read_users():
    user_keys = redis.keys()
    app.logger.info(user_keys)
    return Response(json.dumps({'message' : 'Read users from redis'}), 200)

@app.route('/new_user')
def new_user():


    time.sleep(5)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
