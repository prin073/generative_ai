##  RAG with Queue -  The one we built in 13_rag is a simple synchronous RAG application without any queue. 
# In this one we are going to use Redis Queue(RQ) to create a queue for the RAG application.
# This will make the pipeline asynchronous and scalable. We can add multiple workers to process the queue and make the application faster.


# we can start multiple workers to serve different queries at the same time. 
# This will make the application faster and more scalable. We can also use different types of workers to process different types of queries. For example, we can use a worker with GPU to process the queries that require heavy computation and use a worker with CPU to process the queries that require less computation.

# 0. Qdrant db should also be up from 13_rag example as we will be using the same vector db to store the vector embeddings.

# 1. valkey is the replacement of Redis in this case. 
# It is a simple key-value store that can be used to store the vector embeddings. 
# You can use any key-value store like Redis, Memcached, etc. Just change the key-value store in the code accordingly.

# 2. docker compose up -d
# It will start the valkey server in docker container. Valkey will be running on localhost:6379. You can use this server to store the vector embeddings.

# 3. Redis Queue Package(RQ) is a simple Python library for creating queues and processing them in the background with workers.
# It is built on top of Redis and provides a simple API to create queues, add jobs to the queue, and process the jobs with workers.

```md
pip install rq
```

# 4. client contains the connection information to the valkey server. We will use this client to add jobs to the queue and process them with workers.

```md
from redis import Redis
from rq import Queue
q = Queue(connection=Redis(
    host='localhost',
    port=6379
))
```
# 5. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. We will use FastAPI to create the API endpoints for the RAG application.

```md
pip install fastapi
```

Accessible at http://0.0.0.0:8000/

docs  at http://0.0.0.0:8000/docs

# 6. run the main.py file to start the FastAPI server. This will create the API endpoints for the RAG application. You can use these endpoints to add jobs to the queue and process them with workers.

```md
python main.py
```

# 7. At  http://0.0.0.0:8000/docs send /chat request with the following body to test the RAG application.

```json
{
  "query": "JavaScript in External File"
}
```

# 8. To start executing enqueued functions in the background, you need to start a worker from your project's directory. 
# A worker is a process that listens to the queue and processes the jobs as they come in. You can start multiple workers to process the jobs faster.
# The worker will listen to the queue and process the jobs as they come in. You can start multiple workers to process the jobs faster.

```md
cd 14_rag_queue
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES # This is required to avoid the "RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase." error on MacOS.
export RQ_WORKER_CLASS=rq.worker.SimpleWorker
export HF_TOKEN=<your_token> #optional
rq worker --with-scheduler
```

# Examples job ids
# {
  "status": "queued",
  "jobId": "5c41da57-11d4-4c7a-87fb-0f5ce9802754"
}

{
  "status": "queued",
  "jobId": "082f35d0-7447-4b5b-97ea-785405cecc51"
}