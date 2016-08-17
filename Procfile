worker: rqworker --pid /tmp/rq.pid -u redis://$REDIS_PORT_6379_TCP_ADDR:6379
monitor: python lib/monitor.py /tmp/rq.pid
