from time import sleep

import redis
from pydantic_core._pydantic_core import ValidationError
from rsmq.consumer import RedisSMQConsumer
from rsmq import RedisSMQ, cmd

from configuration import TASK_QUEUE_NAME, RESULTS_QUEUE_NAME, service_logger, REDIS_HOST, REDIS_PORT
from data_model.Translation import Translation
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage
from translate import get_translation


class QueueProcessor:
    def __init__(self):
        self.task_queue = RedisSMQ(
            host=REDIS_HOST,
            port=REDIS_PORT,
            qname=TASK_QUEUE_NAME,
        )

        self.results_queue = RedisSMQ(
            host=REDIS_HOST,
            port=REDIS_PORT,
            qname=RESULTS_QUEUE_NAME,
        )

    def process(self, id, message, rc, ts):
        try:
            task_message = TranslationTaskMessage(**message)
            service_logger.info(f"New task {task_message.model_dump()}")
        except ValidationError:
            service_logger.error(f"Not a valid Redis message: {message}")
            return True

        try:
            translations = [get_translation(translation_task) for translation_task in task_message.get_tasks()]
        except BrokenPipeError:
            response = TranslationResponseMessage(
                **task_message.model_dump(),
                translations=[Translation(text=translation.text, language=translation.language_to, success=False,
                                          error_message="Server unavailable") for translation in
                              task_message.get_tasks()])

            self.results_queue.sendMessage(delay=5).message(response.model_dump()).execute()
            return True

        response = TranslationResponseMessage(
            **task_message.model_dump(),
            translations=translations,
        )

        self.results_queue.sendMessage(delay=5).message(response.model_dump()).execute()
        return True

    def subscribe_to_tasks_queue(self):
        print("Translation queue processor started")
        while True:
            try:
                self.task_queue.getQueueAttributes().exec_command()
                self.results_queue.getQueueAttributes().exec_command()

                redis_smq_consumer = RedisSMQConsumer(
                    qname=TASK_QUEUE_NAME,
                    processor=self.process,
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                )
                redis_smq_consumer.run()
            except redis.exceptions.ConnectionError:
                sleep(20)
            except cmd.exceptions.QueueDoesNotExist:
                self.task_queue.createQueue().exceptions(False).execute()
                self.results_queue.createQueue().exceptions(False).execute()


if __name__ == "__main__":
    queue_processor = QueueProcessor()
    queue_processor.subscribe_to_tasks_queue()
