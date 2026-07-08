from redis import Redis
from rq import Queue

#will store the queries
q = Queue(connection=Redis(
    host='localhost',
    port=6379,
))

