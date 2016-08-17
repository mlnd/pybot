import requests
import time
from redis import StrictRedis
from rq import Queue
from slackclient import SlackClient

new_user_message = """
Hey there, since you're new here, have a look at our Welcome Document:
<https://mlnd.slack.com/files/geekman2/F1U3FJ883/Welcome_to_the_Team>
I know this is an automated response, but we honestly care, which is why we made it.
Enjoy your time here and feel free to discuss.
Some popular channels are <#C1XKFQ3FE|algorithms>, <#C1G4M943B|datawrangling>, <#C0K6TTRCG|deeplearning>, and <#C0HU17DPE|kaggle>.
When you are ready check out <#C0EQ8SUF6|supervised-learning>, <#C0EQKMUQN|unsupervised-learning>, and <#C0K448LBC|reinforcementlearning>
Ask for help with a project here: <#C216N6XSL|p0-introduction>, <#C216N4ATA|p1-boston-housing>, <#C0EQFGYU8|p2-student-interventi>, <#C0M9K8K5M|p3-customer_segments>, <#C21583TEX|p4-train-self-driving>
"""

redis = StrictRedis(host='redis')
q = Queue(connection=redis)

def heartbeat():
    q.enqueue(heartbeat)
    q.enqueue(count_words_at_url, 'http://google.com')
    requests.get('http://requestb.in/1f5ncty1')
    time.sleep(5)
    return "bump bump"

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

def test_on_joshua():
    redis = StrictRedis(host='redis')
    token = "xoxp-14830125314-69227002053-69665825555-3c4a5c84e1"
    this_slack_client = SlackClient(token)
    open_im = this_slack_client.api_call("im.open", user='U0KL2S477')
    this_slack_client.api_call(
        "chat.postMessage",
        channel="general",
        text="test",
        username='pybot',
        icon_emoji=':panda_face:'
    )

def welcome_new_users():
    redis = StrictRedis(host='redis')
    token = "xoxp-14830125314-69227002053-70095041232-6d27a9c4cf"
    this_slack_client = SlackClient(token)

    users = this_slack_client.api_call("users.list")
    current_users = {user['id']:user['name'] for user in users['members']}

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
