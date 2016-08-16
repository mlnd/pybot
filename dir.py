from redis import StrictRedis
import threading
import requests
import os

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        print(item['channel'], ":", item['data'])

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print(self, "unsubscribed and finished")
                break
            else:
                self.work(item)

if __name__ == "__main__":  
    r = StrictRedis(host='redis')
    client = Listener(r, ['test'])
    client.start()
