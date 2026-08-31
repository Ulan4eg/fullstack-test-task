from celery import Celery
from ..core.config import settings

celery_app = Celery(
    "file_tasks",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 минут
    task_soft_time_limit=240,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_annotations={
        'scan_file': {'rate_limit': '10/m'},
        'extract_file_metadata': {'rate_limit': '20/m'},
    },
)

# Автоматическое обнаружение задач
celery_app.autodiscover_tasks(['src.infrastructure.task_queue'])