from celery import Celery
import os

print(f"Initializing Celery app...{os.environ.get('DEVELOPMENT')}")
celery_app = Celery(
    "worker",
    broker="sqs://" if os.environ.get("DEVELOPMENT") != "true" else "redis://127.0.0.1:6379/0",
    backend=None,
)

celery_app.conf.update(
    broker_transport_options={
        "region": "ap-south-1"
    },
    task_routes={
        'tasks.code_generation_tasks.*': {'queue': 'code_generation_queue'},
        'tasks.video_rendering_tasks.*': {'queue': 'video_render_queue'},
    }
)

from worker.tasks import code_generation_tasks, video_rendering_tasks