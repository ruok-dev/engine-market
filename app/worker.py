from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL)
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND

# Import tasks so they are registered
import app.tasks.inventory

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Check inventory every hour
    sender.add_periodic_task(3600.0, app.tasks.inventory.check_low_stock.s(), name='check-low-stock-every-hour')
