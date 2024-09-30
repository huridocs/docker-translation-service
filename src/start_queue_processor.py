import os

from ml_cloud_connector.MlCloudConnector import MlCloudConnector
from pydantic_core._pydantic_core import ValidationError
from queue_processor.QueueProcessor import QueueProcessor

from configuration import service_logger, REDIS_HOST, REDIS_PORT, QUEUES_NAMES
from data_model.Translation import Translation
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTask import TranslationTask
from data_model.TranslationTaskMessage import TranslationTaskMessage
from translate import get_translation

from sentry_sdk.integrations.redis import RedisIntegration
import sentry_sdk


def get_empty_translation(translation_task):
    return Translation(
        text="",
        language=translation_task.language_to,
        success=True,
        error_message="",
    )


def get_error_translation(translation_task: TranslationTask, error_message: str):
    return Translation(
        text=translation_task.text,
        language=translation_task.language_to,
        success=False,
        error_message=error_message,
    )


def get_translation_from_task(translation_task: TranslationTask):
    if not translation_task.text.strip():
        return get_empty_translation(translation_task)

    connector = MlCloudConnector("translation")
    translation, finished, error = connector.execute(get_translation, service_logger, translation_task)
    return translation if finished else get_error_translation(translation_task, error)


def process(message):
    try:
        task_message = TranslationTaskMessage(**message)
        service_logger.info(f"New task {task_message.model_dump()}")
    except ValidationError:
        service_logger.error(f"Not a valid Redis message: {message}")
        return None

    return TranslationResponseMessage(
        **task_message.model_dump(),
        translations=[get_translation_from_task(task_message) for task_message in task_message.get_tasks()],
    ).model_dump()


if __name__ == "__main__":
    try:
        sentry_sdk.init(
            os.environ.get("SENTRY_DSN"),
            traces_sample_rate=0.1,
            environment=os.environ.get("ENVIRONMENT", "development"),
            integrations=[RedisIntegration()],
        )
    except Exception:
        pass

    queues_names = QUEUES_NAMES.split(" ")
    queue_processor = QueueProcessor(REDIS_HOST, REDIS_PORT, queues_names, service_logger)
    queue_processor.start(process)
