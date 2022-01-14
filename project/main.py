from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from . import tasks

app = FastAPI()

REQUEST_COUNT = Counter(
    "request_counter",
    "Count of requests",
    ["request_from"]
)


@app.get("/home")
def run():
    REQUEST_COUNT.labels("home").inc()
    tasks.task_test.delay()
    return {"result": True}


@app.get("/fail")
def fail():
    REQUEST_COUNT.labels("fail").inc()
    tasks.task_fail.delay()
    return {"result": False}


@app.post("/ftp")
def ftp():
    REQUEST_COUNT.labels("ftp").inc()
    tasks.ftp_collector.delay()
    return {"result": False}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)
