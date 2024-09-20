import os
from pydantic_core._pydantic_core import ValidationError
from queue_processor.QueueProcessor import QueueProcessor

from configuration import service_logger, REDIS_HOST, REDIS_PORT, QUEUES_NAMES
from data_model.Translation import Translation
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage
from translate import get_translation

from sentry_sdk.integrations.redis import RedisIntegration
import sentry_sdk


def process(message):
    try:
        task_message = TranslationTaskMessage(**message)
        service_logger.info(f"New task {task_message.model_dump()}")
    except ValidationError:
        service_logger.error(f"Not a valid Redis message: {message}")
        return None

    try:
        translations = [get_translation(translation_task) for translation_task in task_message.get_tasks()]
    except BrokenPipeError:
        response = TranslationResponseMessage(
            **task_message.model_dump(),
            translations=[
                Translation(
                    text=translation.text,
                    language=translation.language_to,
                    success=False,
                    error_message="Server unavailable",
                )
                for translation in task_message.get_tasks()
            ],
        )

        return response.model_dump()

    response = TranslationResponseMessage(
        **task_message.model_dump(),
        translations=translations,
    )

    return response.model_dump()


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
