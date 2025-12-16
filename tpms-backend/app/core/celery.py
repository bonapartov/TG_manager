from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "tpms",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.services.telegram.tasks",
        "app.services.publication.tasks",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    beat_schedule={
        "check-expired-invite-links": {
            "task": "app.services.telegram.tasks.check_expired_invite_links",
            "schedule": 86400,  # Every 24 hours
        },
        "cleanup-old-tasks": {
            "task": "app.services.publication.tasks.cleanup_old_tasks",
            "schedule": 3600,  # Every hour
        },
    },
)

# Set default queue
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_routes = {
    "app.services.telegram.tasks.*": {"queue": "telegram"},
    "app.services.publication.tasks.*": {"queue": "publication"},
}