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
token = "#TOKEN#"
this_slack_client = SlackClient(token)

new_user_message = """
Hey there, since you're new here, have a look at our Welcome Document:
<https://mlnd.slack.com/files/geekman2/F1U3FJ883/Welcome_to_the_Team>
I know this is an automated response, but we honestly care, which is why we made it.
Enjoy your time here and feel free to discuss.
Some popular channels are <#C1XKFQ3FE|algorithms>, <#C1G4M943B|datawrangling>, <#C0K6TTRCG|deeplearning>, and <#C0HU17DPE|kaggle>.
When you are ready check out <#C0EQ8SUF6|supervised-learning>, <#C0EQKMUQN|unsupervised-learning>, and <#C0K448LBC|reinforcementlearning>
Ask for help with a project here: <#C216N6XSL|p0-introduction>, <#C216N4ATA|p1-boston-housing>, <#C0EQFGYU8|p2-student-interventi>, <#C0M9K8K5M|p3-customer_segments>, <#C21583TEX|p4-train-self-driving>
"""

_context = zmq.Context()
_publisher = _context.socket(zmq.PUB)
url = 'tcp://{}:{}'.format('127.0.0.1', '4444')


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
    users = this_slack_client.api_call("users.list")
    current_users = {user['id']:user['name'] for user in users['members']}
    print(current_users)
    with open('users.txt', 'r') as users_file:
        known_users = users_file.read().splitlines()
    new_users = set(current_users) - set(known_users)
    print(new_users)
    for new_user in new_users:
        open_im = this_slack_client.api_call("im.open", user=new_user)
        channel_to_new_user = open_im['channel']['id']
        this_slack_client.api_call(
            "chat.postMessage",
            channel=channel_to_new_user,
            text=new_user_message,
            username='pybot',
            icon_emoji=':robot_face:'
        )

        this_slack_client.api_call(
            "chat.postMessage", channel="#general",
            text="Welcome to the Team! <@{}|{}>".format(new_user,current_users[new_user]),
            username='pybot', icon_emoji=':robot_face:'
        )

    time.sleep(5)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
