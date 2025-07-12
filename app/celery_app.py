from celery import Celery
import os

celery_app = Celery(
    "worker",
    broker="sqs://" if os.environ.get("DEVELOPMENT") != "true" else "redis://localhost:6379/0",
    backend=None,
)

celery_app.conf.update(
    broker_transport_options={
        "region": "ap-south-1"
    }
)
