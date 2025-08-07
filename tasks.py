import os
from logging import INFO, basicConfig

from celery import Celery
from kombu.utils.url import safequote

from ai.config import Env

env = Env()
aws_access_key = safequote(env.aws_client_id)
aws_secret_key = safequote(env.aws_secret)


broker_url = f"sqs://{aws_access_key}:{aws_secret_key}@"


celery_app = Celery("tasks", broker=broker_url)


# broker_transport_options = {
#     "celery-queue": {
#         "my-q": {
#             "url": env.aws_sqs,
#             "access_key_id": aws_access_key,
#             "secret_access_key": aws_secret_key,
#         }
#     },
# }
# celery_app.conf.broker_transport_options = broker_transport_options

celery_app.autodiscover_tasks(["ai.tasks.execute_workflow_node_task"])

# Create logs directory if it doesn't exist and determine log path
log_dir = "/app/logs" if os.path.exists("/app") else "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "tasks.log")

basicConfig(
    filename=log_path,
    level=INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
