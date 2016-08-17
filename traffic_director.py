from redis import Redis
from rq import Queue
from lib.slack_pybot import count_words_at_url, test_on_joshua

q = Queue(connection=Redis())

result = q.enqueue(count_words_at_url, 'http://nvie.com')
result = q.enqueue(test_on_joshua)
