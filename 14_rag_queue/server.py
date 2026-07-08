from fastapi import FastAPI, Query
from clients.rq_client import q
from queues.worker import process_query

app = FastAPI()

@app.get('/')
def root():
    return {"status": "Server is up and running"}

#... (called Ellipsis in Python) is used by FastAPI to indicate: This parameter is REQUIRED
@app.post("/chat")
def chat(query: str = Query(..., description='The chat query of the user')):
    # enque the query to the RAG queue and return a response
    # For demonstration purposes, we will just return the query back as the response
    # below line is where we enqueue the query to the RAG queue.
    # The worker will pick up the query from the queue and process it using the process_query function defined in the worker.py file.
    job = q.enqueue(process_query, query) #stores the query in the queue and returns a job object that contains the id of the job and other metadata. The worker will use this id to track the status of the job and return the response once the job is processed.
    return {"status": "queued",  "jobId": job.id}


@app.get("/jobResult")
def get_result(job_id: str=Query(..., description='The job id of the job')):
    job = q.fetch_job(job_id) #fetch the job from the queue using the job id
    return {
        "status": job.get_status(),
        "response": job.result
    }
