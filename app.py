import json
import os
import time

from flask import Flask, jsonify, request, redirect, url_for, Response
from redis import StrictRedis
from rq import Queue
from slackclient import SlackClient

from lib.pybot import count_words_at_url, heartbeat

app = Flask(__name__)
redis = StrictRedis(host='redis')
q = Queue(connection=redis)

@app.route('/')
def api_live():
    """ root endpoint; serves to notify that the application is live """
    return Response(json.dumps({'message' : 'Api is live.'}), 200)

@app.route('/jumpstart')
def jumpstart():
    result = q.enqueue(count_words_at_url, 'http://nvie.com')
    result = q.enqueue(heartbeat)
    return Response(json.dumps({'message' : "It's alive!"}), 200)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
