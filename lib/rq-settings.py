import os

REDIS_URL = 'redis://'+os.environ['REDIS_PORT_6379_TCP_ADDR']+':6379'
